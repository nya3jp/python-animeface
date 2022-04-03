// Copyright 2013 Shuhei Takahashi
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <Python.h>

// PIL
#include <Imaging.h>

// nvxs
#include "nv_core.h"
#include "nv_ip.h"
#include "nv_ml.h"
#include "nv_face.h"

#define NV_MAX_FACE 4096

#define NV_C2V(x) ((float)((unsigned int)x))

typedef struct {
  PyObject_HEAD
  Imaging image;
  ImagingAccess access;
} ImagingObject;


static void convert_imaging_to_nv(
    Imaging im,
    nv_matrix_t* bgr,
    nv_matrix_t* gray) {
  int y, x;

  assert(strcmp(im->mode, "RGB") == 0 || strcmp(im->mode, "L") == 0);

  if (strcmp(im->mode, "RGB") == 0) {
    for (y = 0; y < im->ysize; ++y) {
      for (x = 0; x < im->xsize; ++x) {
        UINT8* p = (UINT8*)&IMAGING_PIXEL_RGB(im, x, y);
        NV_MAT3D_V(bgr, y, x, NV_CH_R) = NV_C2V(p[0]);
        NV_MAT3D_V(bgr, y, x, NV_CH_G) = NV_C2V(p[1]);
        NV_MAT3D_V(bgr, y, x, NV_CH_B) = NV_C2V(p[2]);
      }
    }
    nv_gray(gray, bgr);
  } else {  // strcmp(im->mode, "L") == 0
    for (y = 0; y < im->ysize; ++y) {
      for (x = 0; x < im->xsize; ++x) {
        UINT8* p = (UINT8*)&IMAGING_PIXEL_L(im, x, y);
        NV_MAT3D_V(bgr, y, x, NV_CH_R) = NV_C2V(p[0]);
        NV_MAT3D_V(bgr, y, x, NV_CH_G) = NV_C2V(p[0]);
        NV_MAT3D_V(bgr, y, x, NV_CH_B) = NV_C2V(p[0]);
        NV_MAT3D_V(gray, y, x, 0) = NV_C2V(p[0]);
      }
    }
  }
}

static int do_detect(
    nv_matrix_t* bgr,
    nv_matrix_t* gray,
    nv_face_position_t* faces,
    int num_max_faces) {
  static const nv_mlp_t* detector_mlp = &nv_face_mlp_face_00;
  static const nv_mlp_t* face_mlp[] = {
    &nv_face_mlp_face_01,
    &nv_face_mlp_face_02,
    NULL
  };
  static const nv_mlp_t* dir_mlp = &nv_face_mlp_dir;
  static const nv_mlp_t* parts_mlp = &nv_face_mlp_parts;

  int num_faces;
  nv_rect_t image_size;
  nv_matrix_t* smooth = nv_matrix3d_alloc(1, bgr->rows, bgr->cols);
  nv_matrix_t* edge = nv_matrix3d_alloc(1, bgr->rows, bgr->cols);
  nv_matrix_t* gray_integral = nv_matrix3d_alloc(1, bgr->rows + 1, bgr->cols + 1);
  nv_matrix_t* edge_integral = nv_matrix3d_alloc(1, bgr->rows + 1, bgr->cols + 1);

  nv_matrix_zero(smooth);
  nv_matrix_zero(edge);
  nv_matrix_zero(gray_integral);
  nv_matrix_zero(edge_integral);

  nv_gaussian5x5(smooth, 0, gray, 0);
  nv_laplacian1(edge, smooth, 4.0f);

  nv_integral(gray_integral, gray, 0);
  nv_integral(edge_integral, edge, 0);

  image_size.x = image_size.y = 0;
  image_size.width = bgr->cols;
  image_size.height = bgr->rows;

  num_faces = nv_face_detect(
      faces,
      num_max_faces,
      gray_integral,
      edge_integral,
      &image_size,
      dir_mlp,
      detector_mlp,
      face_mlp,
      2,
      parts_mlp,
      4.0,    /* step */
      1.095,  /* scale_factor */
      42.592  /* min_window_size */);

  nv_matrix_free(&smooth);
  nv_matrix_free(&edge);
  nv_matrix_free(&gray_integral);
  nv_matrix_free(&edge_integral);

  return num_faces;
}

static PyObject* pack_results(
    nv_face_position_t* faces,
    int num_faces,
    nv_matrix_t* bgr) {
  PyObject* result = PyList_New(num_faces);
  int i;

  for (i = 0; i < num_faces; ++i) {
    PyObject* one_result = PyDict_New();
    nv_face_position_t* face = &faces[i];
    nv_face_feature_t face_feature = {0};
    nv_face_analyze(&face_feature, face, bgr);

    PyDict_SetItemString(
        one_result, "likelihood",
        Py_BuildValue("f", face->likelihood));
    PyDict_SetItemString(
        one_result, "face_box",
        Py_BuildValue(
            "(iiii)",
            face->face.x, face->face.y,
            face->face.width, face->face.height));
    PyDict_SetItemString(
        one_result, "skin_color",
        Py_BuildValue(
            "(iii)",
            (int)face_feature.skin_bgr.v[2],
            (int)face_feature.skin_bgr.v[1],
            (int)face_feature.skin_bgr.v[0]));
    PyDict_SetItemString(
        one_result, "hair_color",
        Py_BuildValue(
            "(iii)",
            (int)face_feature.hair_bgr.v[2],
            (int)face_feature.hair_bgr.v[1],
            (int)face_feature.hair_bgr.v[0]));
    PyDict_SetItemString(
        one_result, "left_eye_box",
        Py_BuildValue(
            "(iiii)",
            face->left_eye.x, face->left_eye.y,
            face->left_eye.width, face->left_eye.height));
    PyDict_SetItemString(
        one_result, "left_eye_color",
        Py_BuildValue(
            "(iii)",
            (int)face_feature.left_eye_bgr[0].v[2],
            (int)face_feature.left_eye_bgr[0].v[1],
            (int)face_feature.left_eye_bgr[0].v[0]));
    PyDict_SetItemString(
        one_result, "right_eye_box",
        Py_BuildValue(
            "(iiii)",
            face->right_eye.x, face->right_eye.y,
            face->right_eye.width, face->right_eye.height));
    PyDict_SetItemString(
        one_result, "right_eye_color",
        Py_BuildValue(
            "(iii)",
            (int)face_feature.right_eye_bgr[0].v[2],
            (int)face_feature.right_eye_bgr[0].v[1],
            (int)face_feature.right_eye_bgr[0].v[0]));
    PyDict_SetItemString(
        one_result, "mouth_box",
        Py_BuildValue(
            "(iiii)",
            face->mouth.x, face->mouth.y,
            face->mouth.width, face->mouth.height));
    PyDict_SetItemString(
        one_result, "nose_point",
        Py_BuildValue(
            "(ii)",
            face->nose.x, face->nose.y));
    PyDict_SetItemString(
        one_result, "chin_point",
        Py_BuildValue(
            "(ii)",
            face->chin.x, face->chin.y));

    PyList_SetItem(result, i, one_result);
  }

  return result;
}

static PyObject* detect(
    PyObject* self,
    PyObject* args) {
  PyObject* result;
  ImagingObject* imobj;
  Imaging im;
  int num_faces;
  nv_matrix_t* bgr;
  nv_matrix_t* gray;
  nv_face_position_t faces[NV_MAX_FACE];

  if (!PyArg_ParseTuple(args, "O", &imobj)) {
    return NULL;
  }
  im = imobj->image;

  bgr = nv_matrix3d_alloc(3, im->ysize, im->xsize);
  gray = nv_matrix3d_alloc(1, im->ysize, im->xsize);
  nv_matrix_zero(bgr);
  nv_matrix_zero(gray);

  convert_imaging_to_nv(im, bgr, gray);

  num_faces = do_detect(bgr, gray, faces, NV_MAX_FACE);

  result = pack_results(faces, num_faces, bgr);

  nv_matrix_free(&bgr);
  nv_matrix_free(&gray);

  return result;
}

static PyMethodDef methods[] = {
  {"detect", (PyCFunction)detect, METH_VARARGS, NULL},
  {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3

static PyModuleDef module = {
  PyModuleDef_HEAD_INIT,
  "animeface._nvxs",
  NULL,
  0,
  methods,
  NULL,
  NULL,
  NULL,
  NULL
};

PyMODINIT_FUNC PyInit__nvxs(void) {
  return PyModule_Create(&module);
}

#else  // PY_MAJOR_VERSION >= 3

PyMODINIT_FUNC init_nvxs(void) {
  Py_InitModule("animeface._nvxs", methods);
}

#endif  // PY_MAJOR_VERSION >= 3

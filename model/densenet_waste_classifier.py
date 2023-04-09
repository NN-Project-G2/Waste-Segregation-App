import os
import numpy as np
import cv2
import tensorflow as tf

from sqlalchemy.orm import Session

import models, schemas


model = tf.keras.models.load_model("model/weights/new_model_denseNet169.h5")
db = Session()


def predict_class(img_np_arr, user_id):
    if not isinstance(img_np_arr, np.ndarray):
        return False, None

    classes=["cardboard","glass","metal","paper","plastic","trash"]
    user_pred = schemas.UserPredictionCreate

    img_np_arr = np.resize(img_np_arr, (224, 224, 3))

    if len(img_np_arr) != 4:
        img_np_arr = np.reshape(img_np_arr, [1, 224, 224, 3])

    pred = model.predict(img_np_arr)
    pred_max_prob_class = np.max(pred)
    pred = pred.tolist()[0]

    pred_class_idx = pred.index(pred_max_prob_class)
    pred_class = classes[pred_class_idx]

    # db_pred = models.UserPrediction(
    #     user_id=user_id,
    #     image_s3_path="in memory",
    #     predicted_label=pred_class,
    #     actual_label=pred_class
    # )
    # db.add(db_pred)
    # db.commit()
    # db.refresh(db_pred)

    return True, pred_class
    

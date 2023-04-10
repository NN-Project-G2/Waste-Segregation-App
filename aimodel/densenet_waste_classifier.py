import os
import numpy as np
import cv2
import tensorflow as tf
from random import randint
from datetime import datetime

from sqlalchemy.orm import Session

import models, schemas
from database_manager import SessionLocal
from aws_manager import *


model = tf.keras.models.load_model("aimodel/weights/waste_classifier_model_denseNet169.h5")


def predict_class(img_np_arr, user_id):
    if not isinstance(img_np_arr, np.ndarray):
        return False, None, None

    classes=["cardboard","glass","metal","paper","plastic","trash"]
    db = SessionLocal()

    img_input = np.resize(img_np_arr, (224, 224, 3))

    if len(img_input) != 4:
        img_input = np.reshape(img_input, [1, 224, 224, 3])

    pred = model.predict(img_input)
    pred_max_prob_class = np.max(pred)
    pred = pred.tolist()[0]

    pred_class_idx = pred.index(pred_max_prob_class)
    pred_class = classes[pred_class_idx]

    s3_path = f"{user_id}/images/{randint(11111111, 99999999)}_{datetime.utcnow().strftime('%d%M%Y_%H%m%S')}.jpg"
    upload_status = upload_file(img_np_arr, s3_path)

    if not upload_status:
        s3_path="in memory"

    db_pred = models.UserPrediction(
        user_id=user_id,
        image_s3_path=s3_path,
        predicted_label=pred_class,
        actual_label=pred_class
    )
    db.add(db_pred)
    db.commit()

    return True, pred_class, db_pred.id
    

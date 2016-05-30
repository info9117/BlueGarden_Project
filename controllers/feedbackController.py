from flask import request, render_template, redirect, url_for, flash, session
from models.user import *
from models.works import *
from models.farm import *



class FeedbackController:
    @staticmethod
    def addFeedback():
        feedback = []


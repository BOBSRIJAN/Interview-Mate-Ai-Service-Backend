import mongoengine as me

class UserQuestionAnswer(me.Document):
    userid = me.StringField(required=True)
    sessionid = me.StringField(required=True, unique=True)
    Questions = me.ListField(me.DictField())
    totalnumberofquestion = me.IntField(default=0)
    tillQuestioncount = me.IntField(default=0)
    
    def __str__(self):
        return UserQuestionAnswer.userid
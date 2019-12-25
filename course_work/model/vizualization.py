from model.model import db, AnswerTable, QuestionsTable
import plotly
import plotly.graph_objs as go
import json


def visualization_data():
    data = db.session.query(QuestionsTable.Type_question,
                            db.func.count(AnswerTable.User_faculty).label("AnswersQuantity")
                            ).join(AnswerTable, QuestionsTable.Question_id == AnswerTable.QuestionIdFk).group_by(
        QuestionsTable.Type_question).all()

    bar = [
        go.Bar(
            x=[value[0] for value in data],
            y=[value[1] for value in data]
        )
    ]

    return json.dumps(bar, cls=plotly.utils.PlotlyJSONEncoder)

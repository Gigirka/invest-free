import flask
from flask import jsonify, make_response, request

from data import db_session
from data.jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=(
                    'id', 'project_name', 'work_size', 'user_id',  'info', 'date', 'needed_money',
                    'invested_money',
                    'is_finished'))
                    for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)

    return jsonify(
        {
            'jobs': jobs.to_dict(only=(
                'id', 'project_name', 'work_size', 'user_id',  'info', 'date', 'needed_money', 'invested_money',
                'is_finished'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['project_name', 'work_size', 'user_id', 'info', 'needed_money', 'invested_money',
                  'is_finished']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    jobs = Jobs(
        project_name=request.json['project_name'],
        work_size=request.json['work_size'],
        user_id=request.json['user_id'],
        # image=request.json['image'],
        info=request.json['info'],
        # date=request.json['date'],
        needed_money=request.json['needed_money'],
        invested_money=request.json['invested_money'],
        is_finished=request.json['is_finished']
    )
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'id': jobs.id})

from flask import Flask, request, jsonify
from models import db, Task, Comment


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Simple SQLite DB for dev
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/')
def home():
    return "Flask backend is running!"


@app.route('/tasks/<int:task_id>/comments', methods=['POST'])
def create_comment(task_id):
    data = request.get_json()
    
    # Validate JSON presence
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400
    
    # Validate 'content' presence and non-empty (strip whitespace)
    if 'content' not in data or not data['content'].strip():
        return jsonify({'error': 'Content is required and cannot be empty'}), 400
    
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    comment = Comment(content=data['content'], task_id=task_id)
    db.session.add(comment)
    db.session.commit()
    
    return jsonify({'id': comment.id, 'content': comment.content, 'task_id': comment.task_id}), 201


@app.route('/tasks/<int:task_id>/comments/<int:comment_id>', methods=['PUT'])
def update_comment(task_id, comment_id):
    data = request.get_json()
    if not data or 'content' not in data or not data['content'].strip():
        return jsonify({'error': 'Content is required and cannot be empty'}), 400
    
    comment = Comment.query.filter_by(id=comment_id, task_id=task_id).first()
    if not comment:
        return jsonify({'error': 'Comment not found for this task'}), 404
    
    comment.content = data['content']
    db.session.commit()
    return jsonify({'id': comment.id, 'content': comment.content, 'task_id': comment.task_id})


@app.route('/tasks/<int:task_id>/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(task_id, comment_id):
    comment = Comment.query.filter_by(id=comment_id, task_id=task_id).first()
    if not comment:
        return jsonify({'error': 'Comment not found for this task'}), 404
    
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Comment deleted successfully'})


@app.route('/tasks/<int:task_id>/comments', methods=['GET'])
def list_comments(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    comments = Comment.query.filter_by(task_id=task_id).order_by(Comment.created_at).all()
    results = [{'id': c.id, 'content': c.content, 'created_at': c.created_at.isoformat()} for c in comments]
    return jsonify(results)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)

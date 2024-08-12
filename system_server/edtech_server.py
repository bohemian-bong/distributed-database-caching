from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['edtech']

# Existing endpoints

@app.route('/api/instructors', methods=['GET'])
def get_instructors():
    instructors = list(db.instructors.find({}, {'_id': 0}))  # Exclude the MongoDB ID
    return jsonify(instructors)

@app.route('/api/courses', methods=['GET'])
def get_courses():
    courses = list(db.courses.find({}, {'_id': 0}))  # Exclude the MongoDB ID
    return jsonify(courses)

@app.route('/api/instructors/<int:id>', methods=['GET'])
def get_instructor_by_id(id):
    instructor = db.instructors.find_one({'id': id}, {'_id': 0})
    if instructor:
        return jsonify(instructor)
    return jsonify({'error': 'Instructor not found'}), 404

@app.route('/api/courses/<int:id>', methods=['GET'])
def get_course_by_id(id):
    course = db.courses.find_one({'id': id}, {'_id': 0})
    if course:
        return jsonify(course)
    return jsonify({'error': 'Course not found'}), 404

@app.route('/api/courses/instructor/<int:instructor_id>', methods=['GET'])
def get_courses_by_instructor(instructor_id):
    courses = list(db.courses.find({'instructors_id': instructor_id}, {'_id': 0}))
    return jsonify(courses)

# New endpoints (previously defined)

# 1. Get all instructors with courses
@app.route('/api/instructors-with-courses', methods=['GET'])
def get_instructors_with_courses():
    instructors_with_courses = []
    for instructor in db.instructors.find({}, {'_id': 0}):
        courses = list(db.courses.find({'instructors_id': instructor['id']}, {'_id': 0}))
        instructor['courses'] = courses
        instructors_with_courses.append(instructor)
    return jsonify(instructors_with_courses)

# 2. Get courses with instructor details
@app.route('/api/courses-with-instructors', methods=['GET'])
def get_courses_with_instructors():
    courses_with_instructors = []
    for course in db.courses.find({}, {'_id': 0}):
        instructor = db.instructors.find_one({'id': course['instructors_id']}, {'_id': 0})
        course['instructor'] = instructor
        courses_with_instructors.append(course)
    return jsonify(courses_with_instructors)

# 3. Get courses with a minimum rating
@app.route('/api/courses/rating/<float:rating>', methods=['GET'])
def get_courses_with_min_rating(rating):
    courses = list(db.courses.find({'rating': {'$gte': rating}}, {'_id': 0}))
    return jsonify(courses)

# 4. Get instructors by job title
@app.route('/api/instructors/job-title/<string:job_title>', methods=['GET'])
def get_instructors_by_job_title(job_title):
    instructors = list(db.instructors.find({'job_title': job_title}, {'_id': 0}))
    return jsonify(instructors)

# 5. Get courses created after a specific date
@app.route('/api/courses/created-after/<string:date>', methods=['GET'])
def get_courses_created_after(date):
    from datetime import datetime
    date_obj = datetime.fromisoformat(date)
    courses = list(db.courses.find({'created': {'$gte': date_obj}}, {'_id': 0}))
    return jsonify(courses)

# 6. Get the number of courses taught by each instructor
@app.route('/api/instructors/course-count', methods=['GET'])
def get_instructor_course_count():
    instructor_course_counts = []
    for instructor in db.instructors.find({}, {'_id': 0}):
        count = db.courses.count_documents({'instructors_id': instructor['id']})
        instructor_course_counts.append({'instructor': instructor, 'course_count': count})
    return jsonify(instructor_course_counts)

# 7. Get all courses with a specific keyword in the title
@app.route('/api/courses/keyword/<string:keyword>', methods=['GET'])
def get_courses_by_keyword(keyword):
    courses = list(db.courses.find({'title': {'$regex': keyword, '$options': 'i'}}, {'_id': 0}))
    return jsonify(courses)

# 8. Get the latest course added
@app.route('/api/courses/latest', methods=['GET'])
def get_latest_course():
    latest_course = db.courses.find_one(sort=[('created', -1)], projection={'_id': 0})
    return jsonify(latest_course)

# 9. Get the average rating of all courses
@app.route('/api/courses/average-rating', methods=['GET'])
def get_average_rating():
    pipeline = [
        {'$group': {'_id': None, 'averageRating': {'$avg': '$rating'}}}
    ]
    result = list(db.courses.aggregate(pipeline))
    return jsonify(result)

# 10. Get instructors with no courses
@app.route('/api/instructors/no-courses', methods=['GET'])
def get_instructors_no_courses():
    instructors_with_courses = [instructor['id'] for instructor in db.instructors.find({}, {'id': 1})]
    instructors = list(db.instructors.find({'id': {'$nin': instructors_with_courses}}, {'_id': 0}))
    return jsonify(instructors)

# New combined endpoints

# 11. Get instructors and the count of their courses
@app.route('/api/instructors/course-counts', methods=['GET'])
def get_instructors_with_course_counts():
    instructors_with_counts = []
    for instructor in db.instructors.find({}, {'_id': 0}):
        count = db.courses.count_documents({'instructors_id': instructor['id']})
        instructor['course_count'] = count
        instructors_with_counts.append(instructor)
    return jsonify(instructors_with_counts)

# 12. Get instructors who teach a specific course
@app.route('/api/instructors/teaching-course/<int:course_id>', methods=['GET'])
def get_instructors_teaching_course(course_id):
    course = db.courses.find_one({'id': course_id}, {'_id': 0})
    if course:
        instructor = db.instructors.find_one({'id': course['instructors_id']}, {'_id': 0})
        return jsonify({'course': course, 'instructor': instructor})
    return jsonify({'error': 'Course not found'}), 404

# 13. Get all courses grouped by instructor
@app.route('/api/courses/grouped-by-instructor', methods=['GET'])
def get_courses_grouped_by_instructor():
    instructors_courses = {}
    for course in db.courses.find({}, {'_id': 0}):
        instructor_id = course['instructors_id']
        instructor = db.instructors.find_one({'id': instructor_id}, {'_id': 0})
        if instructor:
            if instructor['name'] not in instructors_courses:
                instructors_courses[instructor['name']] = []
            instructors_courses[instructor['name']].append(course)
    return jsonify(instructors_courses)

# 14. Get courses taught by instructors with a specific job title
@app.route('/api/courses/job-title/<string:job_title>', methods=['GET'])
def get_courses_by_instructors_job_title(job_title):
    instructors = list(db.instructors.find({'job_title': job_title}, {'id': 1}))
    instructor_ids = [instructor['id'] for instructor in instructors]
    courses = list(db.courses.find({'instructors_id': {'$in': instructor_ids}}, {'_id': 0}))
    return jsonify(courses)

# 15. Get all instructors with their courses and average course rating
@app.route('/api/instructors/courses/average-rating', methods=['GET'])
def get_instructors_with_courses_and_average_rating():
    instructors_with_details = []
    for instructor in db.instructors.find({}, {'_id': 0}):
        courses = list(db.courses.find({'instructors_id': instructor['id']}, {'_id': 0}))
        instructor['courses'] = courses
        if courses:
            average_rating = sum(course['rating'] for course in courses) / len(courses)
            instructor['average_rating'] = average_rating
        else:
            instructor['average_rating'] = 0
        instructors_with_details.append(instructor)
    return jsonify(instructors_with_details)

if __name__ == '__main__':
    app.run(debug=True)

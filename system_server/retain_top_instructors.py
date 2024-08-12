import sys
from pymongo import MongoClient

def retain_top_instructors(n):
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['edtech']

    # Step 1: Aggregate the Courses by Instructor ID
    instructor_course_counts = db.courses.aggregate([
        {
            "$group": {
                "_id": "$instructors_id",
                "course_count": { "$sum": 1 }
            }
        },
        { "$sort": { "course_count": -1 } },  # Sort by course count in descending order
        { "$limit": n }  # Limit to top n instructors
    ])

    # Step 2: Extract Instructor IDs
    top_instructor_ids = [instructor["_id"] for instructor in instructor_course_counts]

    # Step 3: Delete Instructors Not in the Top n
    db.instructors.delete_many({ "id": { "$nin": top_instructor_ids } })

    # Step 4: Delete Courses Not Associated with the Top n Instructors
    db.courses.delete_many({ "instructors_id": { "$nin": top_instructor_ids } })

    print(f"Retained top {n} instructors and their courses.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python retain_top_instructors.py <n>")
        sys.exit(1)
    
    
    n = int(sys.argv[1])

    retain_top_instructors(n)

import requests
import random
import sys
import time

BASE_URL = "http://localhost:5000/api"

# List of all available endpoints
endpoints = [
    "/instructors",
    "/courses",
    "/instructors/<int:id>",
    "/courses/<int:id>",
    "/courses/instructor/<int:instructor_id>",
    "/instructors-with-courses",
    "/courses-with-instructors",
    "/courses/rating/<float:rating>",
    "/instructors/job-title/<string:job_title>",
    "/courses/created-after/<string:date>",
    "/instructors/course-count",
    "/courses/keyword/<string:keyword>",
    "/courses/latest",
    "/courses/average-rating",
    "/instructors/no-courses",
    "/instructors/course-counts",
    "/instructors/teaching-course/<int:course_id>",
    "/courses/job-title/<string:job_title>",
    "/instructors/courses/average-rating"
]

course_id = [
    567828, 1362070,  950390,  903744, 1754098,  258316,
    354176,  705264,  382002, 1430746, 1708340, 1576854,
    1793828,  765242,  822444, 2473048, 1352468,  959700,
    1151632, 1419182
]

instructor_id = [
    9685726, 31926668,  2364054, 8280056, 33027212,  5997742,
    5487312,   712832, 38516954, 35101150, 13363166, 16122994,
    6772884, 21681922, 13148312, 8735380,   710121, 33231436,
    598757, 29951918
]

job_title = [
    'Adobe Certified Instructor & Adobe Certified Expert',
    'Agribusiness simplified for farmers across Africa and beyond',
    'Alternative Medicine Expert',
    'Amazing online courses to unleash your creativity',
    'An Google, Facebook, Kaggle Grandmasters team',
    'An ex-Google, Stanford and Flipkart team',
    'Android Developer/Designer',
    'Android, Flutter, AWS, Best Selling Instructor',
    'Animation Courses for Beginners',
    'Appassionato Ingegnere Informatico Best Seller',
    'Apple Featured iOS Developer and iOS Instructor',
    'Apps Games Unity iOS Android Apple Watch TV Development',
    'Arq. PMP. MATI   Autodesk Educator Expert',
    'Art Classes, Mentoring & Inspiration!',
    'Art Instructor, Professional Painter, Writer',
    'Art and paper crafting teacher',
    'Artificial Intelligence and Business Transformation Experts',
    'Artificial intelligence and machine learning engineer',
    'Artist & Designer',
    'Artist & Educator',
    'Associate Professor of Commerce',
    'Author, Publisher and Educator',
    'Author, YouTuber, Keynote & TEDx Speaker, CEO Rule the Room',
    'Avid, Steinberg Certified Audio Engineer, Instructor',
    'Award Winning Instructors, 100,000+ students'
]

keyword = ["Python", "Java", "C++", "React", "Web"]

dates = [
    "2016-01-05", "2016-03-22", "2016-06-15", "2016-09-09", "2016-12-25",
    "2017-02-11", "2017-05-06", "2017-07-19", "2017-10-03", "2017-12-30",
    "2018-01-20", "2018-03-14", "2018-06-02", "2018-08-25", "2018-11-12",
    "2016-02-17", "2017-04-08", "2018-05-28", "2016-07-04", "2017-09-13"
]

# Helper function to send a request to a random endpoint
def send_random_request():
    endpoint = random.choice(endpoints)

    # Replacing placeholders with random or sample values
    endpoint = endpoint.replace("courses/<int:id>", "courses/" + str(random.choice(course_id)))
    endpoint = endpoint.replace("instructors/<int:id>", "instructors/" + str(random.choice(instructor_id)))
    endpoint = endpoint.replace("<int:instructor_id>", str(random.choice(instructor_id)))
    endpoint = endpoint.replace("<int:course_id>", str(random.choice(course_id)))
    endpoint = endpoint.replace("<float:rating>", str(random.uniform(1, 5)))
    endpoint = endpoint.replace("<string:job_title>", str(random.choice(job_title)))
    endpoint = endpoint.replace("<string:keyword>", str(random.choice(keyword)))
    endpoint = endpoint.replace("<string:date>", random.choice(dates))
    
    url = BASE_URL + endpoint

    start_time = time.time()
    try:
        response = requests.get(url)
        elapsed_time = time.time() - start_time
        print(f"Request to {url} returned status code {response.status_code}")
        return elapsed_time
    except requests.exceptions.RequestException as e:
        print(f"Request to {url} failed: {e}")
        return None

# Main function to send n random requests and calculate time statistics
def send_n_random_requests(n):
    total_time = 0
    successful_requests = 0
    max_time = 0
    min_time = float('inf')

    for _ in range(n):
        elapsed_time = send_random_request()
        if elapsed_time is not None:
            total_time += elapsed_time
            successful_requests += 1
            if elapsed_time > max_time:
                max_time = elapsed_time
            if elapsed_time < min_time:
                min_time = elapsed_time

    if successful_requests > 0:
        average_time = total_time / successful_requests
        print(f"\nTotal time taken for {successful_requests} requests: {total_time:.2f} seconds")
        print(f"Average time per request: {average_time:.2f} seconds")
        print(f"Highest time for a single request: {max_time:.2f} seconds")
        print(f"Lowest time for a single request: {min_time:.2f} seconds")
    else:
        print("No successful requests were made.")

# Run the script with n as a command-line argument
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <n>")
        sys.exit(1)

    n = int(sys.argv[1])
    send_n_random_requests(n)

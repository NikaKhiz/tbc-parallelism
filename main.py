import requests, json, threading, time
from queue import Queue

url = "https://jsonplaceholder.typicode.com/posts/{}"
num_of_posts = 77
posts_queue = Queue()
file_lock = threading.Lock()

def main():
    start_time = time.perf_counter()
    
    fetch_posts_using_threads()
    write_to_a_file('posts.json')
    
    end_time = time.perf_counter()
    print(f"Time taken: {end_time - start_time:.2f} seconds")


# fetch post from url and put it in queue
def fetch_post(post_id):
    try:
        response = requests.get(url.format(post_id))
        post_data = response.json()
        posts_queue.put(post_data)
    except requests.RequestException as e:
        print(f"Error fetching post {post_id}: {e}")


# use threading for time efficiency
def fetch_posts_using_threads():
    threads = []
    for post_id in range(1, num_of_posts + 1):
        thread = threading.Thread(target=fetch_post, args=(post_id,))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

# write data from queue in to the file
def write_to_a_file(filename):
    with file_lock:
        all_posts = []
        while not posts_queue.empty():
            all_posts.append(posts_queue.get())
        
        all_posts.sort(key=lambda post: post['id'])
        with open(filename, 'w') as file:
            json.dump(all_posts, file, indent=4)


if __name__ == "__main__":
    main()

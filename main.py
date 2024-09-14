import requests, json, threading, time
from concurrent.futures import ThreadPoolExecutor

url = "https://jsonplaceholder.typicode.com/posts/{}"
num_of_posts = 77
lock = threading.Lock()
num_of_posts_written = 1

def main():
    start_time = time.perf_counter()
    
    fetch_posts_using_threads()
    
    end_time = time.perf_counter()
    print(f"Time taken: {end_time - start_time:.2f} seconds")


# fetch post from url according to given post id and write it directly in to the file 
def fetch_and_write(post_id):
    global num_of_posts_written

    try:
        response = requests.get(url.format(post_id))
        with lock:
            with open('posts.json', 'a') as file:
                json.dump(response.json(), file, indent=4)

                # increase number of posts written
                # to append necessary characters in to the file
                num_of_posts_written += 1
                
                if num_of_posts_written <= num_of_posts:
                    file.write(',\n')
                else:
                    file.write('\n]')

    except requests.RequestException as e:
        print(f"Error fetching post {post_id}: {e}")


# truncate file content and set its initial state
# use threadpoolexecutor for fetching multiple posts simultaneously
def fetch_posts_using_threads():
    with open('posts.json', 'a') as file:
            file.seek(0)
            file.truncate()
            file.write('[\n')

    with ThreadPoolExecutor(max_workers=15) as executor:
        executor.map(fetch_and_write, range(1, num_of_posts + 1))


if __name__ == "__main__":
    main()

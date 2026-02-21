import requests
from requests.auth import HTTPBasicAuth
domain="https://mansipandey.in/"

your_username='mehwish'
your_password='find it from your whatsapp'

def read_all_posts():
    endpoint="wp-json/wp/v2/posts"
    url=domain+endpoint
    response = requests.get(url).json()

    for item in response:
        print(f' ID:{item.get("id")} Post Title: {item.get("title")["rendered"]}  Link: -> {item.get("link")}')

    # return response



def create_post(title, content, status="draft"):
    data = {
        "title": title,
        "content": content,
        "status": status
    }
    response = requests.post(
        domain + "/wp-json/wp/v2/posts",
        json=data,
        auth=HTTPBasicAuth(your_username, your_password)
    )
    print(response.json().get("id"))

def delete_post(post_id, force=True):
    response = requests.delete(
        domain + f"/wp-json/wp/v2/posts/{post_id}",
        params={"force": str(force).lower()},
        auth=HTTPBasicAuth(your_username, your_password)
    )
    print(response.json())

def get_post(post_id):
    response = requests.get(domain + f"/wp-json/wp/v2/posts/{post_id}")
    post = response.json()
    print(f" LINK:{ post.get('link')}")
    print(f" TITLE:{ post.get('title')['rendered']}")
    print(f" CONTENT:{ post.get('content')['rendered']}")
    print("----")

def update_post(post_id, title=None, content=None, status=None):
    data = {}
    if title:
        data["title"] = title
    if content:
        data["content"] = content
    if status:
        data["status"] = status

    response = requests.post(
        domain + f"/wp-json/wp/v2/posts/{post_id}",
        json=data,
        auth=HTTPBasicAuth(your_username, your_password)
    )
    print(response.json())


if __name__ == "__main__":
    # read_all_posts()


    # post_id = "27"
    # update_post(post_id, title="Guardian of Galaxy", status= "publish" )
    # get_post(post_id)

    # create_post("myname is akhilesh", "i do stuff randomaly", status="publish")

    post_do_delete= 31
    delete_post(post_do_delete)


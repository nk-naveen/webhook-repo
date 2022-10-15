from flask import request, render_template, Blueprint
from app.extensions import MongoConnect


webhook = Blueprint('webhook', __name__)

# Endpoint


@webhook.route('/receiver', methods=['POST'])
def receiver():
    if request.headers['content_type'] == 'application/json':
        git_post_data = request.json  
        if git_post_data.get("ref"):
            branch = git_post_data.get("ref")
            action = ["PUSH"]  #action as PUSH
            request_id = git_post_data["commits"][0]["id"]
            author = git_post_data["commits"][0]["author"]["name"]
            # Time of the commit
            timestamp = git_post_data["commits"][0]["timestamp"]
            from_branch = branch[11:]  #From branch
            to_branch = from_branch  #PUSH method
            data = {
                'request_id': request_id,
                'author': author,
                'action': action,
                'from_branch': from_branch,
                'to_branch': to_branch,
                'timestamp': timestamp
            }
            obj = MongoConnect(data)
            obj.write(data)
            return {}, 200

        # For PULL request
        elif git_post_data.get("action") == 'opened':
            action = ["PULL"]
            request_id = git_post_data["sender"]["id"]
            author = git_post_data["sender"]["login"]
            timestamp = git_post_data["pull_request"]["updated_at"]
            from_branch = git_post_data["repository"]["default_branch"]
            to_branch = git_post_data["pull_request"]["title"]
            data = {
                'request_id': request_id,
                'author': author,
                'action': action,
                'from_branch': from_branch,
                'to_branch': to_branch,
                'timestamp': timestamp
            }
            obj = MongoConnect(data)
            obj.write(data)
            return {}, 200

        # For MERGE request
        elif git_post_data.get("action") == 'synchronize':
            action = ["MERGE"]
            request_id = git_post_data["sender"]["id"]
            author = git_post_data["sender"]["login"]
            timestamp = git_post_data["pull_request"]["updated_at"]
            from_branch = git_post_data["repository"]["default_branch"]
            to_branch = git_post_data["pull_request"]["title"]
            data = {
                'request_id': request_id,
                'author': author,
                'action': action,
                'from_branch': from_branch,
                'to_branch': to_branch,
                'timestamp': timestamp
            }
            obj = MongoConnect(data)
            obj.write(data)
            return {}, 200
        #check only for [PUSH, PULL, MERGE] and skipping other operations.
        else:
            return {}, 200

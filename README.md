# burndown-chart-gitlab
python script that generates a burndown-chart of a gitlab project


# How to setup
clone the repository 
```sh 
git clone 
```

install dependencies
```sh
pip install -r requirments.txt
```

in config.json file fill in:
```json
{
    "link": "gitlab_link",
    "access_token": "gitlab_access_token",
    "project_path": "path_to_repository",
    "discord_token": "discord_token"
}
```


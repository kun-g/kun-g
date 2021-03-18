import os
from datetime import datetime
from github import Github
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

TOKEN = os.environ.get("MY_GITHUB_TOKEN", "")
g = Github(TOKEN)

ignores = [
        "ChenjinyanX/subject-openmanual", 
        "kun-g/allergism", 
        "kun-g/emergency_storage_list",
        "kun-g/ever-dungeon-data",
        "kun-g/going-to-production",
        "kun-g/hexo-theme-A-RSnippet",
        "kun-g/IA06_FA",
        "kun-g/IATB",
        "kun-g/KuBiTionAdvanture",
        "kun-g/learning-node",
        "kun-g/little-ninja-rush",
        "kun-g/NodeNote",
        "kun-g/reading",
        "kun-g/reading-track",
        "kun-g/screeps",
        "kun-g/sketch",
        "kun-g/snake",
        "kun-g/solid-guacamole",
        "kun-g/subject-openmanual",
        "kun-g/techradar",
        "kun-g/til",
        "kun-g/Trimps.github.io",
        "lava-hammer/allergy_log",
        "TrinGame/art",
        "TrinGame/black-box-ever-dungeon",
        "TrinGame/client",
        "TrinGame/data-ever-dungeon",
        "TrinGame/server",

        "kun-g/csapp-reading-notes", # No Lang
        "kun-g/kun-g", # No Lang
        ]

languages = {
    # Logo, URL, COLOR, LogoColor
    'Python': ('python', 'https://www.python.org/', '3C78A9', 'FFFFFF'),
    'JavaScript': ('javascript', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript', 'F1E05A', 'FFFFFF'),
    'Node.js': ('node.js', 'https://nodejs.org/en/', '47d147', 'FFFFFF'),
    'C++': ('C++', 'https://isocpp.org/', 'ff751a', 'FFFFFF'),
    'Swift': ('Swift', 'https://swift.org/', 'fa7343', 'FFFFFF'),
}
def group_by(data, key):
    res = {}
    for item in data:
        if item[key] not in res:
            res[item[key]] = []
        res[item[key]].append(item)
    return res

with open('./stack.yml', 'r') as f:
    config = load(f, Loader=Loader)
    print(config)

def build_stack():
    repos = []
    for repo in g.get_user().get_repos():
        if repo.full_name in ignores:
            continue
        lang = list(repo.get_languages().items())
        lang.sort(key=lambda e:e[1], reverse=True)
        lang = lang[0][0]
        if lang not in languages:
            print(f"Missing language {lang}: {repo.url}")
            continue
        working = (datetime.now() - repo.updated_at).days < 30
        repos.append({ 'url': repo.url, 'wip': working, 'lang': lang })
    groups = group_by(repos, 'lang')
    stack = []
    for lang in groups:
        repos = groups[lang]
        logo, url, color, logoColor = languages[lang]
        item = {
                'name': lang, 
                'logo': logo, 
                'url':  url,
                'color': color,
                'logoColor': logoColor,
                'projects': []
        }
        for l in repos:
            del l['lang']
            item['projects'].append(l)
        stack.append(item)

    with open('./stack.yml', 'w') as of:
        of.write(dump(stack, Dumper=Dumper))

build_stack()

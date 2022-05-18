###
# adapted from https://github.com/Guzpenha/MANtIS/blob/master/csearch/builders/json_builder.py
# and https://github.com/Guzpenha/MANtIS/blob/master/csearch/converters/pandas2json.py
###

from pandas import DataFrame
import pandas as pd
import numpy as np
from math import floor
from xml2pandas import XML2Pandas
import re
import html
from markdownify import markdownify as md
import os

CLEANR = re.compile('<.*?>')


def generate_dataframe(data_path, ):
    print('Fetching XML files from ' + data_path)
    # Generate the dataframe for posts and comments
    posts_df = XML2Pandas(os.path.join(data_path , 'Posts.xml')).convert()
    votes_df = XML2Pandas(os.path.join(data_path , 'Votes.xml')).convert()
    users_df = XML2Pandas(os.path.join(data_path , 'Users.xml')).convert()
    spam_votes_df = votes_df.loc[votes_df['VoteTypeId'].isin(['4', '12'])].copy()

    # Convert necessary columns to numeric
    posts_df['Id'] = pd.to_numeric(posts_df['Id'], downcast='integer')
    posts_df['OwnerUserId'] = pd.to_numeric(posts_df['OwnerUserId'], downcast='integer')
    posts_df['ParentId'] = pd.to_numeric(posts_df['ParentId'], downcast='integer')
    posts_df['AcceptedAnswerId'] = pd.to_numeric(posts_df['AcceptedAnswerId'], downcast='integer')
    posts_df['Score'] = pd.to_numeric(posts_df['Score'], downcast='integer')

    users_df['Id'] = pd.to_numeric(users_df['Id'], downcast='integer')
    spam_votes_df['PostId'] = pd.to_numeric(spam_votes_df['PostId'], downcast='integer')

    print('Merging the information...')
    posts_df = posts_df.loc[~posts_df['OwnerUserId'].isnull()]

    filtered_posts_df = pd.merge(
        posts_df,
        spam_votes_df,
        how='left',
        left_on='Id',
        right_on='PostId',
        suffixes=('_post', '_votes')
    )
    filtered_posts_df = filtered_posts_df.loc[filtered_posts_df['PostId'].isnull()]

    columns = ['AcceptedAnswerId', 'Body', 'CreationDate_post', 'Id_post', 'OwnerUserId', 'ParentId', 'PostTypeId',
               'Score', 'Title', "AnswerCount", "FavoriteCount", "Tags"]
    filtered_posts_df = filtered_posts_df[columns]

    posts_users_df = pd.merge(
        filtered_posts_df,
        users_df,
        how='left',
        left_on='OwnerUserId',
        right_on='Id',
        suffixes=('_post', '_user')
    )

    columns = ['AcceptedAnswerId', 'Body', 'CreationDate_post', 'Id_post', 'OwnerUserId', 'ParentId', 'PostTypeId',
               'Score', 'Title', "AnswerCount", "FavoriteCount", "Tags", "DisplayName", 'Location', 'AboutMe']
    posts_users_df = posts_users_df[columns]

    filtered_df = posts_users_df.reset_index(drop=True)

    # Sort by post creation date and then by comment
    filtered_df = filtered_df.sort_values(by=['CreationDate_post'])

    return filtered_df


def process_text(text):
    markdown = md(text)
    text = html.unescape(text)
    unescape_text = text
    no_dup = re.sub('<blockquote>\n  <p><strong>Possible Duplicate:.*?</a>  </p>\n</blockquote>\n', ' ', text,
                    flags=re.DOTALL)

    c_text = re.sub('<(?!blockquote)(?!pre)(?!code)(?!/blockquote)(?!/pre)(?!/code).*?>', '',
                    no_dup).replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    c_text = CLEANR.sub("", c_text)
    c_text = re.sub(r'\s+', ' ', c_text)

    if not c_text:
        c_text = ''
    if not markdown:
        markdown = ''
    if not unescape_text:
        unescape_text = ''

    return [c_text.strip(), unescape_text, markdown]


def generate_dict(df, mode):
    item = {}
    item['Title'] = str(df['Title'])
    if mode == 'plain':
        item['Body'] = str(process_text(df['Body'])[0])
    elif mode == "markdown":
        item['Body'] = str(process_text(df['Body'])[2])
    elif mode == "unescape":
        item['Body'] = str(process_text(df['Body'])[1])
    item['Score'] = df['Score']
    item['Favorite_Count'] = df['FavoriteCount']
    item['CreationDate'] = df['CreationDate_post']
    item['OriginalPostId'] = df['Id_post']
    item['User_Id'] = df['OwnerUserId']
    item['Display_Name'] = df['DisplayName']
    if not pd.isna(df['AboutMe']):
        if mode == 'plain':
            item['User_About_Me'] = process_text(df['AboutMe'])[0]
        elif mode == "markdown":
            item['User_About_Me'] = process_text(df['AboutMe'])[2]
        elif mode == "unescape":
            item['User_About_Me'] = process_text(df['AboutMe'])[1]
    else:
        item['User_About_Me'] = str(df['AboutMe'])
    item['Location'] = df['Location']

    return item


def generate_QA(df, maps):
    df = df[df['Body'].notna()]

    original_posts_df = df.loc[df['PostTypeId'] == '1'].drop_duplicates('Id_post')
    original_posts_df = original_posts_df.reset_index(drop=True)

    responses_df = df.loc[(df['PostTypeId'] == '2')].drop_duplicates('Id_post')
    responses_df = responses_df.reset_index(drop=True)

    total_progress_increment = floor(original_posts_df.shape[0] / 100)

    counter = 0
    data = {}
    data_m = {}
    data_u = {}
    for progress_index, original_post in original_posts_df.iterrows():
        if progress_index % total_progress_increment == 0 and floor(progress_index / total_progress_increment) < 100:
            print('Progress: ' + str(floor(progress_index / total_progress_increment)) + '%')

        original_post_id = original_post['Id_post']
        current_responses_df = responses_df.loc[responses_df['ParentId'] == original_post_id]
        ent = generate_dict(original_post, 'plain')
        ent_m = generate_dict(original_post, 'markdown')
        ent_u = generate_dict(original_post, 'unescape')
        tags_str = original_post['Tags']
        tags_str = tags_str.replace('<', '')
        tags_list = tags_str.split(">")
        tags_list = list(filter(None, tags_list))
        ent["Tags"] = tags_list
        ent_m["Tags"] = tags_list
        ent_u["Tags"] = tags_list
        ent["Answers"] = []
        ent_m["Answers"] = []
        ent_u["Answers"] = []
        if ent['Body'] == '':
            print("WARNING: empty Q body")
        responses_sorted = current_responses_df.sort_values(by=['Score'], ascending=False)
        for index, response in responses_sorted.iterrows():
            rep = generate_dict(response, 'plain')
            rep_m = generate_dict(response, 'markdown')
            rep_u = generate_dict(response, 'unescape')
            if rep['Body'] == '':
                print("WARNING: empty A body")
                continue
            del rep['Title']
            del rep_m['Title']
            del rep_u['Title']
            rep['is_accepted'] = (response['Id_post'] == original_post['AcceptedAnswerId'])
            rep_m['is_accepted'] = (response['Id_post'] == original_post['AcceptedAnswerId'])
            rep_u['is_accepted'] = (response['Id_post'] == original_post['AcceptedAnswerId'])
            ent["Answers"].append(rep)
            ent_m["Answers"].append(rep_m)
            ent_u["Answers"].append(rep_u)

        data[maps[str(ent['OriginalPostId'])]] = ent
        data_m[maps[str(ent['OriginalPostId'])]] = ent_m
        data_u[maps[str(ent['OriginalPostId'])]] = ent_u
        counter += 1

    return data, data_m, data_u

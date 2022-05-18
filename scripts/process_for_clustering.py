import json
import os
from xml2pandas import XML2Pandas
import networkx as nx
import argparse


def to_graph(l):
    G = nx.Graph()
    for part in l:
        # each sublist is a bunch of nodes
        nx.add_path(G, part)
    return list(nx.connected_components(G))


def read_xlm(path, name, links):
    if name == 'eng':
        name = 'english'
    posts_df = XML2Pandas(os.path.join(path, name + '.stackexchange.com', 'PostLinks.xml')).convert()

    for index, row in posts_df.iterrows():
        if row['LinkTypeId'] == "3":
            links.append([row['PostId'], row['RelatedPostId']])

    G = to_graph(links)
    # print(G)
    for i in range(len(G)):
        G[i] = list(G[i])

    return G


def read_data(path):
    ids = []
    with open(path) as f:
        data = json.load(f)
    for id in data:
        QA = data[id]
        ids.append([str(QA['OriginalPostId'])])

    return ids, data


def write_clusters(name, links, data, p):
    path = os.path.join(p, 'clustering')
    counter = 1
    new_links = []
    for ii in range(len(links)):
        new_links.append([])
        for jj in range(len(links[ii])):
            if links[ii][jj] in data.keys():
                new_links[-1].append(links[ii][jj])
        if len(new_links[-1]) < 2:
            del new_links[-1]

    for ii in range(len(new_links)):
        if not os.path.exists(os.path.join(path, name)):
            os.makedirs(os.path.join(path, name))
        with open(os.path.join(path, name, 'C_' + str(counter) + '.tsv'), 'w') as outp:
            counter += 1
            for jj in range(len(new_links[ii])):
                ind = new_links[ii][jj]
                if ind in data.keys():
                    outp.write(data[ind]['id'] + '\t' + data[ind]['t'] + '\t' + data[ind]['b'] + '\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, required=True)
    args = parser.parse_args()
    for filename in os.listdir(args.data_dir):
        new_dict = {}
        if "simple" in filename and '-' not in filename:
            site = filename.split('.')[0]
            bd = set()
            ids, data = read_data(os.path.join(args.data_dir, filename))
            for current_id in data:
                if data[current_id]["Body"] in bd:
                    continue
                org = str(data[current_id]['OriginalPostId'])
                new_dict[org] = {}
                new_dict[org]['id'] = site + '_' + str(current_id)
                new_dict[org]['t'] = data[current_id]["Title"]
                new_dict[org]['b'] = data[current_id]["Body"]
                bd.add(data[current_id]["Body"])

            graph = read_xlm(args.data_dir, site, [])
            write_clusters(site, graph, new_dict, args.data_dir)

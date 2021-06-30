import yaml

def join(loader, node):
    seq = loader.construct_sequence(node)
    return ''.join([str(i) for i in seq])

yaml.add_constructor('!join', join)

with open(r'D:\evanarose.com\_data\demo.yml') as file:
    data = yaml.load(file, Loader=yaml.FullLoader)

with open(r'D:\evanarose.com\_data\rev_demo.yml', 'w') as outfile:
    yaml.dump(data, outfile, default_flow_style=False)
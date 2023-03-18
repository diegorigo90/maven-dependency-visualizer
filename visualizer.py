import os
import xml.etree.ElementTree as ElementTree
import networkx as nx
import matplotlib.pyplot as plt

MAVEN_VERSION = '{http://maven.apache.org/POM/4.0.0}'
PROJECT_DIR = './project'

G = nx.DiGraph()

for root, dirs, files in os.walk(PROJECT_DIR):
    for file in files:
        if file == 'pom.xml':
            tree = ElementTree.parse(os.path.join(root, file))
            root = tree.getroot()

            project_group_id = root.find(MAVEN_VERSION + 'groupId').text
            project_artifact_id = root.find(MAVEN_VERSION + 'artifactId').text

            G.add_node(f'{project_group_id}:{project_artifact_id}')

            dependencies = root.findall('.//' + MAVEN_VERSION + 'dependency')

            for dependency in dependencies:
                dependency_group_id = dependency.find(MAVEN_VERSION + 'groupId').text
                dependency_artifact_id = dependency.find(MAVEN_VERSION + 'artifactId').text

                G.add_node(f'{dependency_group_id}:{dependency_artifact_id}')
                G.add_edge(f'{project_group_id}:{project_artifact_id}',
                           f'{dependency_group_id}:{dependency_artifact_id}')

nx.draw(G, with_labels=True)
plt.show()

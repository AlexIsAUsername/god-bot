import mchmm as mc


input_file = "kjvc.txt" 



the_bible = None

with open(input_file) as f:
    the_bible = f.readline()
    

# print(the_bible.split(" "))

chain = mc.MarkovChain().from_data(the_bible.split(" "))

print("Done creating chain")

graph = chain.graph_make(
    format="png",
    graph_attr=[("rankdir", "LR")],
    node_attr=[("fontname", "Roboto bold"), ("fontsize", "20")],
    edge_attr=[("fontname", "Iosevka"), ("fontsize", "12")]
)
graph.render()

print(chain)


# CosmosAnalyzer
Network analysis of Cosmos Hub

This project should be intended as an extension of the DiLeNA project developed by the AnaNSi research group which provides a software able to retrieve the transactions stored in the distributed ledger of different DLTs, create an abstraction of a network and then measure some related metrics.\\
The project is composed of two main components:
- **Graph Downloader**: it is in charge of downloading the transactions of the examined DLT, generated during the time interval of interest. Then, a directed graph is built, that represents the interactions among the nodes. The vertices of the graph correspond to the addresses in the DLT and, for each transaction, an edge directed from the sender to the recipient of the transactions is made (if not already existing)
- **Graph Analyzer**: is in charge of calculating the typical metrics related to the obtained graph. Among the others, the tool is able to measure the degree distribution, network clustering coefficient, as well as to identify the main component and some of its main metrics, such as the average shortest path. Moreover, the tool computes if the network is a small world, by comparing it with a corresponding random graph (with the same amount of nodes and edges)

Starting from the software already available, this specific extension project provide further studies on a different crypto. In particular, the focus is on the Cosmos ecosystem, a decentralized network of independent parallel blockchain powered by BFT consensus. Among the blockchain present within the ecosystem, the cosmos-hub blockchain will be analyzed: it is the first Hub launched in the Cosmos Network and it is a Proof-of-Stake public blockchain whose native token is called ATOM, and where transaction fees are payable in multiple tokens.

Structure of the project:

![alt text](https://github.com/AndreP-git/CosmosAnalyzer/blob/master/diagram.png?raw=true)

More info regarding technical details and results can be found in the pdf report.

import React from "react";
import Graph from "react-vis-network-graph"

export default function Cite(){
    const data={
      "Citeref": [
          {
              "Main_Paper": "5678",
              "Name": "Emerging Trends in Blockchain Technology",
              "PaperID": "5678901",
              "Year": 1999
          },
          {
              "Main_Paper": "5678",
              "Name": "Data Privacy in the Cloud",
              "PaperID": "6789012",
              "Year": 1999
          },
          {
              "Main_Paper": "5678",
              "Name": "Ethical Considerations in AI Development",
              "PaperID": "7890123",
              "Year": 2001
          },
          {
              "Main_Paper": "1234567",
              "Name": "Document Retrieval on Repetitive Collections",
              "PaperID": "5678",
              "Year": 1994
          },
          {
              "Main_Paper": "2345678",
              "Name": "Advanced Machine Learning Techniques",
              "PaperID": "5678",
              "Year": 1995
          },
          {
              "Main_Paper": "5678901",
              "Name": "Advancements in Quantum Computing",
              "PaperID": "8901234",
              "Year": 2005
          },
          {
              "Main_Paper": "6789012",
              "Name": "Deep Learning Applications in Finance",
              "PaperID": "9012345",
              "Year": 2007
          },
          {
              "Main_Paper": "7890123",
              "Name": "Advancements in Quantum Computing",
              "PaperID": "8901234",
              "Year": 2005
          },
          {
              "Main_Paper": "8901234",
              "Name": "Deep Learning Applications in Finance",
              "PaperID": "9012345",
              "Year": 2007
          },
          {
              "Main_Paper": "3456789",
              "Name": "Optimization Strategies for Robotics",
              "PaperID": "1234567",
              "Year": 1992
          },
          {
              "Main_Paper": "1234567",
              "Name": "Document Retrieval on Repetitive Collections",
              "PaperID": "2345678",
              "Year": 1994
          },
          {
              "Main_Paper": "3456789",
              "Name": "Optimization Strategies for Robotics",
              "PaperID": "2345678",
              "Year": 1992
          },
          {
              "Main_Paper": "4567890",
              "Name": "Neural Networks in Healthcare",
              "PaperID": "2345678",
              "Year": 1990
          },
          {
              "Main_Paper": "4567890",
              "Name": "Neural Networks in Healthcare",
              "PaperID": "3456789",
              "Year": 1990
          },
          {
              "Main_Paper": "3456789",
              "Name": "Optimization Strategies for Robotics",
              "PaperID": "1234567",
              "Year": 1992
          }
      ],
      "Name": "AI Governance: Policy and",
      "Paper": "5678",
      "Year": 1997
  }
    const initializeGraph = () => {
        const graph = {
          nodes: [],
          edges: []
        };
    
        // Add the main paper node
        const mainPaperId = data["Paper"];
        graph.nodes.push({
          id: mainPaperId,
          label: `node ${mainPaperId}`,
          title: `node ${mainPaperId}`,
          x: 0,
          y: 0
        });


        data["Citeref"].forEach(citation => {
          const paperId = citation["PaperID"];
          const MainPaperID = citation["Main_Paper"];
          const year = citation["Year"];
          const diff=year-data["Year"]

          if (!graph.nodes.find(node => node.id === paperId)) {
            const randomX = Math.floor(Math.random() * 201) - 100;
            graph.nodes.push({
              id: paperId,
              label: `node ${paperId}`,
              title: `node ${paperId}`,
              x: randomX, 
              y: diff*20
            });
          }
          
          graph.edges.push({
            from: citation["Main_Paper"],
            to: paperId
          });
        });
        data["Citeref"].forEach(citation => {
          const paperId = citation["Main_Paper"];
          const year = citation["Year"];
          const diff=year-data["Year"]

          if (!graph.nodes.find(node => node.id === paperId)) {
            const randomX = Math.floor(Math.random() * 201) - 100;
            graph.nodes.push({
              id: paperId,
              label: `node ${paperId}`,
              title: `node ${paperId}`,
              x: randomX, 
              y: diff*20
            });
          }
        });
    
        return graph;
      };
    
      const options={
        edges:{
            color:"yellow"
        },
        physics: false,
        height: "900px",
        nodes:{
            borderWidth:2,
            size:40,
            color:{
                border:"#222222",
                background:"#666666"
            },
            font:{color:"yellow"}
        }
    }
      // Initialize graph data
      const graphData = initializeGraph();
    
      return (
        <div>
          <Graph graph={graphData} options={options} /> 
        </div>
      );
    }


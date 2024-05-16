import { useEffect, useState } from 'react'
import React from "react";
import Graph from "react-vis-network-graph"
import { Typography } from "@mui/material"
import Button from '@mui/material/Button'
import TextField from '@mui/material/TextField';
import Card from '@mui/material/Card';
import DenseTable from './table';
import BasicMenu from './menu';

function useData(){
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:5000/paper/testl1/5678', {
          method: 'GET'
        });
        const jsonData = await response.json();
        setData(jsonData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData(); // Initial fetch

    const intervalId = setInterval(fetchData, 1000); // Fetch data every 1000ms

    return () => clearInterval(intervalId); // Cleanup interval on unmount
  }, []);

  return data;
}

const Pimpact=["Scientometrics","Patent citations","Clinical trial citations","Funding data","Social media influence","Nobel prize papers"]




export default function Cite(){
    const data=  {
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
      "Name": "AI Governance: Policy and Strategies",
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
    
      const options = {
        edges: {
          color: "yellow"
        },
        physics: false,
        height: "900px",
        nodes: {
          shape: "circle",
          size: 10,
          color: {
            border: "#222222",
            background: "#666666"
          },
          font: { color: "yellow" }
        }
      };
      // Initialize graph data
      const graphData = initializeGraph();
    
      return (
        <div>
            <div style={{
              display: "flex",
              flexDirection: "column",
              backgroundColor: "lightgray",
              alignItems:"center"
            }}>
              
              <Card variant="outlined" style={{width: 1320,padding:20,margin:5}}>
                <Title Name={data.Name} Year={data.Year} Paper={data.Paper}></Title>
              </Card>

              <Card variant="outlined" style={{width: 1320,padding:20,margin:10,display:"flex",display:"inline-flex"}}>
                <Button size={"large"} variant="outlined" style={{margin:10}}>layer3</Button>
                <Button size={"large"} variant="contained" style={{margin:10}}>cite tree</Button>
                <Button size={"large"} variant="contained" style={{margin:10}}>reference tree</Button>
                <BasicMenu items={Pimpact} name="Paper impact"></BasicMenu>
                <Button size={"large"} variant="contained" style={{margin:10}}>Author impact</Button>
                <Button size={"large"} variant="contained" style={{margin:10}}>Affiliation impact</Button>
              </Card>

              <div style={{ 
                width: "100%", 
                backgroundColor: "orange", 
                display:"flex",
                paddingBottom:10
              }}>
                
                
              <Card variant="outlined" style={{flex: "20%",backgroundColor:"white",display:"flex",flexDirection:"column",alignItems:"center"}}>

                {/* <Conected Name={data.Name} Year={data.Year} Paper={data.Paper}></Conected> */}
                {data.Citeref.map((paper)=>{
                    return <Conected Name={paper.Name} Year={paper.Year} Paper={paper.PaperID}></Conected>
                })}
              </Card>
              <Card variant="outlined" style={{flex: "50%",backgroundColor:"blue"}}>

              </Card>
              <Card variant="outlined" style={{flex: "30%",backgroundColor:"green",padding:10}}>
                <DenseTable/>
              </Card>
                                 
              </div>
            </div>
                  
        </div>
      );
    }
  //   {
  //     "Main_Paper": "3456789",
  //     "Name": "Optimization Strategies for Robotics",
  //     "PaperID": "2345678",
  //     "Year": 1992
  // },
    // {todos.map((todo)=>{
    //   return <Todo title={todo.title} description={todo.description}></Todo>
    // })}
            // {/* <Typography variant={"h6"}>data["Name"]</Typography> */}



            

function Conected(props){
  return <div>
    <Card variant="outlined" style={{width:"250px",backgroundColor:"grey",marginBottom:"10px",marginTop:"10px"}}>
      <h4 style={{margin:5}}>Paper Name:{props.Name}</h4>
      <h5 style={{margin:5}}>Year:{props.Year}</h5>
      <h5 style={{margin:5}}>Paper ID:{props.Paper}</h5>
    </Card>
  </div>
}

function Title(props){
  return <div>
    <Typography variant={"h3"}>Paper Name:{props.Name}</Typography>
    <Typography variant={"h5"}>Paper ID:{props.Paper}</Typography>
    <Typography variant={"h6"}>Year:{props.Year}</Typography>     
  </div>
}

















{/* <div>
            <Graph graph={graphData} options={options} /> 
          </div> */}










  //   {
  //     "Citeref": [
  //         {
  //             "Main_Paper": "5678",
  //             "Name": "Emerging Trends in Blockchain Technology",
  //             "PaperID": "5678901",
  //             "Year": 1999
  //         },
  //         {
  //             "Main_Paper": "5678",
  //             "Name": "Data Privacy in the Cloud",
  //             "PaperID": "6789012",
  //             "Year": 1999
  //         },
  //         {
  //             "Main_Paper": "5678",
  //             "Name": "Ethical Considerations in AI Development",
  //             "PaperID": "7890123",
  //             "Year": 2001
  //         },
  //         {
  //             "Main_Paper": "1234567",
  //             "Name": "Document Retrieval on Repetitive Collections",
  //             "PaperID": "5678",
  //             "Year": 1994
  //         },
  //         {
  //             "Main_Paper": "2345678",
  //             "Name": "Advanced Machine Learning Techniques",
  //             "PaperID": "5678",
  //             "Year": 1995
  //         },
  //         {
  //             "Main_Paper": "5678901",
  //             "Name": "Advancements in Quantum Computing",
  //             "PaperID": "8901234",
  //             "Year": 2005
  //         },
  //         {
  //             "Main_Paper": "6789012",
  //             "Name": "Deep Learning Applications in Finance",
  //             "PaperID": "9012345",
  //             "Year": 2007
  //         },
  //         {
  //             "Main_Paper": "7890123",
  //             "Name": "Advancements in Quantum Computing",
  //             "PaperID": "8901234",
  //             "Year": 2005
  //         },
  //         {
  //             "Main_Paper": "8901234",
  //             "Name": "Deep Learning Applications in Finance",
  //             "PaperID": "9012345",
  //             "Year": 2007
  //         },
  //         {
  //             "Main_Paper": "3456789",
  //             "Name": "Optimization Strategies for Robotics",
  //             "PaperID": "1234567",
  //             "Year": 1992
  //         },
  //         {
  //             "Main_Paper": "1234567",
  //             "Name": "Document Retrieval on Repetitive Collections",
  //             "PaperID": "2345678",
  //             "Year": 1994
  //         },
  //         {
  //             "Main_Paper": "3456789",
  //             "Name": "Optimization Strategies for Robotics",
  //             "PaperID": "2345678",
  //             "Year": 1992
  //         },
  //         {
  //             "Main_Paper": "4567890",
  //             "Name": "Neural Networks in Healthcare",
  //             "PaperID": "2345678",
  //             "Year": 1990
  //         },
  //         {
  //             "Main_Paper": "4567890",
  //             "Name": "Neural Networks in Healthcare",
  //             "PaperID": "3456789",
  //             "Year": 1990
  //         },
  //         {
  //             "Main_Paper": "3456789",
  //             "Name": "Optimization Strategies for Robotics",
  //             "PaperID": "1234567",
  //             "Year": 1992
  //         }
  //     ],
  //     "Name": "AI Governance: Policy and",
  //     "Paper": "5678",
  //     "Year": 1997
  // }
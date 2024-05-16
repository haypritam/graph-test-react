import React from "react";
import Graph from 'react-vis-network-graph'

export default function Graphview(){
    const graph={
        nodes:[
            {id:1, label:"node 1", title:"node 1 i guess",color: "red"},
            {id:2, label:"node 2", title:"node 2 i guess"},
            {id:3, label:"node 3", title:"node 3 i guess"},
            {id:4, label:"node 4", title:"node 4 i guess"},
            {id:5, label:"node 5", title:"node 5 i guess"},
            {id:6, label:"node 6", title:"node 6 i guess"},
            {id:7, label:"node 7", title:"node 7 i guess"},
            {id:8, label:"node 8", title:"node 8 i guess"},
            {id:9, label:"node 9", title:"node 9 i guess"}
        ],
        edges:[
            {from:1, to:2},
            {from:1, to:3},
            {from:2, to:4},
            {from:2, to:5},
            {from:3, to:6},
            {from:3, to:7},
            {from:4, to:8},
            {from:4, to:9}
        ]
    }

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



    return (
        <div className="container">
            <Graph
                graph={graph}
                options={options}
            />
        </div>
    )
}


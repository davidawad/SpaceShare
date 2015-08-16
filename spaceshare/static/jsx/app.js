/** @jsx React.DOM */

var DynamicSearch = React.createClass({

  // sets initial state
  getInitialState: function(){
    return { searchString: '' };
  },

  // sets state, triggers render method
  handleChange: function(event){
    // grab value form input box
    this.setState({searchString:event.target.value});
    console.log("scope updated!");
  },

  render: function() {

    var countries = this.props.items;
    var searchString = this.state.searchString.trim().toLowerCase();

    // filter countries list by value from input box
    if(searchString.length > 0){
      countries = countries.filter(function(country){
        return country.name.toLowerCase().match( searchString );
      });
    }

    return (
      <div>
        <input type="text" value={this.state.searchString} onChange={this.handleChange} placeholder="Search!" />
        <ul>
          { countries.map(function(country){ return <li>{country.name} </li> }) }
        </ul>
      </div>
    )
  }

});

// list of countries, defined with JavaScript object literals
const countries = [
  {"name": "Sweden"}, {"name": "China"}, {"name": "Peru"}, {"name": "Czech Republic"},
  {"name": "Bolivia"}, {"name": "Latvia"}, {"name": "Samoa"}, {"name": "Armenia"},
  {"name": "Greenland"}, {"name": "Cuba"}, {"name": "Western Sahara"}, {"name": "Ethiopia"},
  {"name": "Malaysia"}, {"name": "Argentina"}, {"name": "Uganda"}, {"name": "Chile"},
  {"name": "Aruba"}, {"name": "Japan"}, {"name": "Trinidad and Tobago"}, {"name": "Italy"},
  {"name": "Cambodia"}, {"name": "Iceland"}, {"name": "Dominican Republic"}, {"name": "Turkey"},
  {"name": "Spain"}, {"name": "Poland"}, {"name": "Haiti"}
];

React.render(
  <DynamicSearch items={ countries } />,
  document.getElementById('main')
);

var ProgressBar = React.createClass({

    getInitialState: function(){
        return { progress: "Click Here to see a worker progress",
                 task_id: 0
             } ;
    },

    handleClick: function(event){
        // if the state is 0, start the task
        if(this.state.task_id === 0){
            $.getJSON('/react/task', {} , function(data){
              console.log(data);
              this.state.progress = data.progress;
              this.state.task_id = data.task_id;
            });
        }else{ // we have a task, poll for progress
            $.getJSON('/react/task/'+this.state.task_id.toString(), {} , function(data){
              console.log(data);
              this.state.progress = data.progress;
            });
        }
    },

    render: function(){
        return(
            <div class='exbutton dark center' onClick={this.handleClick}>
                <p>{this.state.progress} </p>
            </div>
            )
    }

});
React.render(
    <ProgressBar/>,
    document.getElementById('prog_bar')
);

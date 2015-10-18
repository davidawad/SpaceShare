/** @jsx React.DOM */

/*
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
          {countries.map(function(country){return <li>{country.name} })}
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
// TODO render search bar component with array of current files
React.render(
  <DynamicSearch items={ countries } />,
  document.getElementById('DynamicSearch')
);



var ProgressBar = React.createClass({

    getInitialState: function(){
        return { progress: "Click Here to see a worker progress",
                 task_id: 0
                };
    },

    handleClick: function(event){
        // if the state is 0, start the task
        if(this.state.task_id === 0){

            $.ajax({
              url: "react/task",
              dataType: 'json',
              success: function(data) {
                console.log(data);
                // TODO more modular way of updating this thing
                this.setState({progress: data.progress, task_id: data.task_id}, function(){
                  this.forceUpdate();
                }.bind(this));
              }.bind(this),
            });
        }else{ // we do have a task, poll for progress
            $.ajax({
              url: "react/task/"+this.state.task_id,
              dataType: 'json',
              success: function(data) {
                console.log(data);

                this.setState({progress: data.state, task_id:data.task_id}, function(){
                // console.log(this.state.data);
                this.forceUpdate();

                }.bind(this));
              }.bind(this),

             error: function(){
                 this.setState({progress: "can't connect to server, check internet connection"});
             }
           });
        }
    },

    render: function(){
        return(
            <div class='exbutton dark center' onClick={this.handleClick}>
                <p>{this.state.progress}</p>
            </div>
            )
    }
});
React.render(
    <ProgressBar/>,
    document.getElementById('ProgressBar')
);
*/

// this creates a React component that can be used in other components or
// used directly on the page with React.renderComponent
var FileForm = React.createClass({
  // since we are starting off without any data, there is no initial value
  getInitialState: function() {
        return {
            task_id: 0,
            data_uri: null,
            progress: "Select an integer to map your file"
        };
  },
  // prevent form from submitting; we are going to capture the file contents
  handleSubmit: function(e) {
    e.preventDefault();
  },
  // when an int is passed into our component, we want to handle the click,
  // and check if the number is reserved on our webserver
  handleInt: function(e){
      var self = this;
      //console.log(e.target.value)
      // find if number is taken
      $.getJSON( "/api/_route_taken", {space:e.target.value}, function(data) {
          // e.g. 62 is taken if in debug mode
          console.log(data);
          if(data.result === parseInt(e.target.value)){
            self.setState({progress: "that's taken"});
          }else{
            self.setState({progress: "you're good"});
        }
      });

  },
  // when a file is passed to the input field, retrieve the contents as a
  // base64-encoded data URI and save it to the component's state
  handleFile: function(e) {
    var self = this;
    var reader = new FileReader();
    var file = e.target.files[0];
    var space = document.getElementById("reserve").value;

    console.log("SpaceReserve request :"+space);
    if(!isNumber(space)){
        self.setState({progress: "Please insert an actual"});
        return;
    }

    reader.onload = function(upload) {
      self.setState({
        data_uri: upload.target.result,
      });
      console.log(upload)
      console.log(upload.target.result)
      /* var file_object = {name: ,
                            data_uri: upload.target.result,
                            };
      $.getJSON('/upload_file', , function(res){}); */

    };
    reader.readAsDataURL(file);
  },
  // return the structure to display and bind the onChange, onSubmit handlers
  render: function() {
    // since JSX is case sensitive, be sure to use 'encType'
    return (
    <center>
     <h2><a href="" class="bree">Open a Space</a></h2>

      <form id="create-form" onSubmit={this.handleSubmit} encType="multipart/form-data">
        <input type="number" name="space" onChange={this.handleInt} id="reserve" placeholder="e.g. '32' "/>
        <input type="file"   name="file"  onChange={this.handleFile}/>
        <input type="submit" name="submit" value="upload" class="radius button create-button"/>

        <p>value: {this.state.progress}</p>
        <p>task_id: {this.state.task_id}</p>
        <p>data_uri: {this.state.data_uri}</p>
      </form>
    </center>
    );
  }
});

React.render(
    <FileForm/>,
    document.getElementById('FileForm')
)

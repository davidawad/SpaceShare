(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);throw new Error("Cannot find module '"+o+"'")}var f=n[o]={exports:{}};t[o][0].call(f.exports,function(e){var n=t[o][1][e];return s(n?n:e)},f,f.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
/** @jsx React.DOM */

var DynamicSearch = React.createClass({displayName: "DynamicSearch",

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
      React.createElement("div", null, 
        React.createElement("input", {type: "text", value: this.state.searchString, onChange: this.handleChange, placeholder: "Search!"}), 
        React.createElement("ul", null, 
           countries.map(function(country){ return React.createElement("li", null, country.name, " ") }) 
        )
      )
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
/* don't render search bar component just yet
React.render(
  <DynamicSearch items={ countries } />,
  document.getElementById('main')
);
*/


/* Defining new component ProgressBar */

var ProgressBar = React.createClass({displayName: "ProgressBar",

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
                // TODO more modular way of updating this dict
                this.setState({progress: data.progress, task_id:data.task_id}, function(){
                  this.forceUpdate();
                }.bind(this));
              }.bind(this),
            });
        }else{ // we do have a task, poll for progress
            $.ajax({
              url: "react/task/"+this.state.task_id.toString(),
              dataType: 'json',
              success: function(data) {
                console.log(data);

                this.setState({progress: data.state, task_id:data.task_id}, function(){
                // console.log(this.state.data);
                this.forceUpdate();

                }.bind(this));
              }.bind(this),
            });
        }
    },

    render: function(){
        return(
            React.createElement("div", {class: "exbutton dark center", onClick: this.handleClick}, 
                React.createElement("p", null, this.state.progress, " ")
            )
            )
    }

});
React.render(
    React.createElement(ProgressBar, null),
    document.getElementById('prog_bar')
);


},{}]},{},[1])
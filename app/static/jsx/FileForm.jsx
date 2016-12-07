// this creates a React component that can be used in other components or
// used directly on the page with React.renderComponent
var FileForm = React.createClass({
  // since we are starting off without any data, there is no initial value
  getInitialState: function() {
        return {
            space: 0,
            data_uri: null,
            status: "Select an integer to map your file",
        };
  },
  // prevent form from submitting; we are going to capture the file contents
  handleSubmit: function(e) {
    e.preventDefault();
  },
  // when an int is passed into our component, we want to handle the change
  // check if the number is reserved on our webserver
  handleInt: function(e){
      var self = this;
      if (!e.target.value){
          self.setState({status: "Please insert a number"});
          return;
      }
      // find if number is taken
      $.getJSON( "/api/_route_taken", {space:e.target.value}, function(data) {
          // e.g. 64 is taken if in debug mode
          console.log(data);
          if(data.result === true){
            self.setState({status: "that's taken", space:e.target.value});
          }else{
            self.setState({status: "you're good", space:e.target.value});
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

    if(typeof space == 'number'){
        self.setState({status: "Please insert a number"});
        return;
    }

    reader.onload = function(upload) {
      self.setState({
        data_uri: upload.target.result,
      });

      console.log(self.state);

      // TODO pass this as a function in a callback
      $.post('/upload_file', self.state , function(res){
            console.log('got a response!!');
            console.log(res);
            if(res.upload === true){
                self.setState({status:'Upload Succeeded!'});
            }else{
                self.setState({status:'upload failed, please try again'});
            }
      });

    };
    reader.readAsDataURL(file);
  },
  // return the structure to display and bind the onChange, onSubmit handlers
  render: function() {
    // since JSX is case sensitive, be sure to use 'encType'
    return (
    <center>
     <h2><a href="" class="bree">Open a Space</a></h2>

      <form onSubmit={this.handleSubmit} encType="multipart/form-data">
        <input type="number" name="space" onChange={this.handleInt} id="reserve" placeholder="e.g. '32' "/>
        <input type="file"   name="file"  onChange={this.handleFile}/>

        <p>value: {this.state.status}</p>
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


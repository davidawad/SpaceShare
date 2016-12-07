import React from 'react';
const $ = require ('jquery')

const buttonStyle = {
    fontFamily: 'Pacifico',
    fontSize:  '2em',
};

class CreateBox extends React.Component {

  constructor(props) {
    super(props);
    this.state = { 
        space_number : 0,
        file_name : '',
        file_data  : '',
        usr_msg: 'Choose a key for your file!'
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleFile   = this.handleFile.bind(this); 
  }

  handleChange(event) {
    this.setState({value: event.target.value});
    
    console.log(event.target.value)

    if (event.target.value === '') {
        console.log('space field is empty')
        return; 
    }
    // take number and perform a lookup
    $.ajax({
      url: '/api/check_space',
      dataType: 'json',
      type: 'POST',
      data: { space_number: event.target.value },
		
      success: function(data) {
		let space_msg = 'This space is free!';
		if (data.result) {
			space_msg = 'Looks like this space is taken.';
		} 
        this.setState({usr_msg: space_msg});
      }.bind(this),

      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
		// update user facing message with server response
	    self.setState({usr_msg: "Failed to connect"})	
      }.bind(this)

    });
	
  }

  handleFile(event) {
    const self = this;

    event.preventDefault();
    let reader = new FileReader();
    let file = event.target.files[0];

    reader.onloadend = function (upload) {
      self.setState({ 
          file_data: file,
          file_name: file.name 
      }); 
    }
    
    reader.readAsDataURL(file);
  }

  handleSubmit(event) {
    event.preventDefault();
	var self = this;
    
    if (this.state.file_name === '' || this.state.file_data === '') {
        alert('no file submitted!');
    }
    
    // try to send file to backend. Report error if upload fails
    $.ajax({
      url: '/api/file_submit',
      dataType: 'json',
      type:     'POST',
      data: self.state,

      success: function(data) {
        this.setState({data: data});
      }.bind(this),

      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
		// update user facing message with server response

      }.bind(this)

    });
  }

  render() {
    return (
      <div className="panel center">

		<h2> <a className="bree">Create a Space</a></h2>
        <form id="create-form" onSubmit={this.handleSubmit} encType="multipart/form-data">
 			<p className="usr_msg"> {this.state.usr_msg} </p>   	
            <input type="number" id="reserve" name="space_number" placeholder="e.g. '32'" value={this.state.value} onChange={this.handleChange}/>
            <input type="file" name="file" onChange={this.handleFile}/>

            <input id="open-button" type="submit" value="upload" className="radius button" style={buttonStyle}/>
		</form>
      </div>
    );
  }
}

export default CreateBox;

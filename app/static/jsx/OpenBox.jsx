import React from 'react';
const $ = require ('jquery')

const buttonStyle = {
    fontFamily: 'Pacifico',
    fontSize:  '2em',
};

class OpenBox extends React.Component {

  constructor(props) {
    super(props);
    this.state = { 
        space_number : 0,
        usr_msg: 'Enter the space for your file!'
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({value: event.target.value});

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
		let space_msg = 'This space is empty';
		if (data.result) {
            // TODO generate snappy response
            // TODO change button styles to indicate download is ready
			space_msg = 'Looks good hoss!';
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

  handleSubmit(event) {
    console.log('User submitted ' + this.state.value + '. Checking status.');
    
    event.preventDefault();
    // user hit submit, download file for them
    // TODO file downloading 
    
  }

  render() {
    return (
      <div className="panel center">

		<h2> <a className="bree">Open a Space</a></h2>
        <form id="create-form" onSubmit={this.handleSubmit}>	
 			<p className="usr_msg"> {this.state.usr_msg} </p>   	
            <input type="number" id="reserve" placeholder="e.g. '32'" value={this.state.value} onChange={this.handleChange}/>

            <input id="open-button" type="submit" value="download" className="radius button" style={buttonStyle}/>
		</form>
      </div>
    );
  }
}

export default OpenBox;

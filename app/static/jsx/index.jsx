import React from 'react';
import {render} from 'react-dom';
import AwesomeComponent from './AwesomeComponent.jsx';
import OpenBox from './OpenBox.jsx'
import CreateBox from './CreateBox.jsx'

/*
 * Main Page Structure.
 * NGINX is serving an older version of these files!
 */

class App extends React.Component {
  render () {
    return (
      <div className="row">
            
        <div className="large-5 columns">
            <CreateBox/>
        </div>

        <div className="large-2 columns"> 
        </div>

        <div className="large-5 columns">
            <OpenBox/>
        </div>

      </div>
    );
  }
}

render(<App/>, document.getElementById('app'));

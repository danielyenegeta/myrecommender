import React from 'react';
import './Navbar.css';
import DrawerToggleButton from '../SideDrawer/DrawerToggleButton';
const toolbar = props => (
  <header className="toolbar">
    <nav className="toolbar__navigation">
      <div className="toolbar__toggle-button">
        <DrawerToggleButton click={props.drawerClickHandler}/>
      </div>
      <div className="toolbar__logo"><a href="/">PIANOSONGS</a></div>
      <div className="spacer" />
      <div className="toolbar__navigationitems">
        <ul>
          <li><a href="/addsong">Add</a></li>
          <li><a href="/removesong">Remove</a></li>
          <li><a href="/home">Homepage</a></li>
          <li><a href="/logout">Logout</a></li>
        </ul>
      </div>
    </nav>
  </header>
);

export default toolbar;

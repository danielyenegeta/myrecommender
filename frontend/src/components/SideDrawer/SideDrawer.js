import React from 'react';
import './SideDrawer.css';

const sideDrawer = props => {
  let drawerClasses = ['side-drawer'];
  if (props.show) {
    drawerClasses = ['side-drawer open'];
  }
  return (
    <nav className={drawerClasses}>
    <ul>
      <li><a href="/addsong">Add</a></li>
      <li><a href="/removesong">Remove</a></li>
      <li><a href="/rate">Rate</a></li>
      <li><a href="/home">Homepage</a></li>
      <li><a href="/logout">Logout</a></li>
    </ul>
  </nav>
  );
};

export default sideDrawer;

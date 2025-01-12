import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import Header from './Header'
import axios from 'axios'

function Layout() {
  return (
    <div className="container">
      <Sidebar />
      <div className="main-content">
        <Header />
        <Outlet />
      </div>
    </div>
  )
}

export default Layout
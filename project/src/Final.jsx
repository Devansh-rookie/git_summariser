import React from 'react'
import { BrowserRouter, Routes, Route,Link} from "react-router-dom";
import App from './App';
import CodeEditor from './CodeEditor';

const Final = () => {
   
  return (
    <BrowserRouter>
      <div>
        <Link to="/">Home</Link>
        <Link to="/codeeditor">Code Editor</Link>
        <Routes>
          <Route path="/" element={<App />} />
          <Route path="/codeeditor" element={<CodeEditor />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default Final
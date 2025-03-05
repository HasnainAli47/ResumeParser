import { useState } from "react";
import { Bars3Icon, XMarkIcon } from "@heroicons/react/24/solid";

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="bg-gradient-to-r from-blue-600 to-purple-600 shadow-lg fixed w-full z-50">
      <div className="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center space-x-3">
            <img src="https://assets.apilayer.com/apis/resume_parser.png" alt="Logo" className="h-8 w-8" />
            <span className="text-white text-2xl font-extrabold tracking-wide">CV Analysis</span>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex space-x-6">
            <a href="/" className="text-white hover:text-gray-300 transition-all duration-200">Upload Resume</a>
            <a href="/search" className="text-white hover:text-gray-300 transition-all duration-200">Search Candidates</a>
            <a href="/chatbot" className="text-white hover:text-gray-300 transition-all duration-200">AI Chatbot</a>
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden">
            <button onClick={() => setIsOpen(!isOpen)} className="text-white focus:outline-none">
              {isOpen ? <XMarkIcon className="h-6 w-6" /> : <Bars3Icon className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <div className="md:hidden bg-blue-700 text-white py-2 space-y-2">
          <a href="/" className="block text-center py-2 hover:bg-blue-800">Upload Resume</a>
          <a href="/search" className="block text-center py-2 hover:bg-blue-800">Search Candidates</a>
          <a href="/chatbot" className="block text-center py-2 hover:bg-blue-800">AI Chatbot</a>
        </div>
      )}
    </nav>
  );
};

export default Navbar;

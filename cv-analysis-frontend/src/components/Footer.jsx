import { FaGithub, FaLinkedin, FaTwitter } from "react-icons/fa";
import { motion } from "framer-motion";

const Footer = () => {
  return (
    <motion.footer
      className="w-full bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 text-white py-8 mt-12 shadow-lg"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <div className="container mx-auto flex flex-col items-center text-center px-6">
        {/* Logo or Title */}
        <h2 className="text-2xl font-semibold tracking-wider text-gray-100">
          CV Analysis System
        </h2>
        <p className="text-sm text-gray-400 mt-1">
          AI-powered search to find the right talent instantly
        </p>

        {/* Social Media Icons */}
        <div className="flex mt-5 space-x-6">
          <a
            href="https://github.com/HasnainAli47"
            target="_blank"
            rel="noopener noreferrer"
            className="text-gray-300 hover:text-blue-400 transition duration-300 transform hover:-translate-y-1"
          >
            <FaGithub size={26} />
          </a>
          <a
            href="https://www.linkedin.com/in/hasnainali3/"
            target="_blank"
            rel="noopener noreferrer"
            className="text-gray-300 hover:text-blue-400 transition duration-300 transform hover:-translate-y-1"
          >
            <FaLinkedin size={26} />
          </a>
        </div>

        {/* Divider */}
        <div className="w-24 h-1 bg-blue-500 rounded-full my-5"></div>

        {/* Links Section */}
        <div className="flex flex-wrap justify-center space-x-6 text-gray-400 text-sm">
          <a href="#" className="hover:text-white transition duration-300">
            Privacy Policy
          </a>
          <a href="#" className="hover:text-white transition duration-300">
            Terms of Service
          </a>
          <a href="#" className="hover:text-white transition duration-300">
            Contact Us
          </a>
        </div>

        {/* Copyright & Info */}
        <p className="text-xs text-gray-500 mt-5">
          © {new Date().getFullYear()} CV Analysis System. All rights reserved.
        </p>
      </div>
    </motion.footer>
  );
};

export default Footer;

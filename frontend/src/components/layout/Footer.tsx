import React from "react";

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gray-900 text-white py-8 mt-auto">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Brand */}
          <div>
            <h3 className="text-xl font-bold mb-2">stockJEDI</h3>
            <p className="text-gray-400 text-sm">
              AI-Powered Stock Intelligence and Investment Analysis Platform
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-lg font-semibold mb-3">Quick Links</h4>
            <ul className="space-y-2 text-gray-400 text-sm">
              <li>
                <a
                  href="https://github.com/denziljosteve/stockJEDI"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-white transition-colors"
                >
                  GitHub Repository
                </a>
              </li>
              <li>
                <a
                  href="http://localhost:8000/docs"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-white transition-colors"
                >
                  API Documentation
                </a>
              </li>
              <li>
                <a
                  href="https://github.com/denziljosteve/stockJEDI/issues"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-white transition-colors"
                >
                  Report Issue
                </a>
              </li>
            </ul>
          </div>

          {/* Author */}
          <div>
            <h4 className="text-lg font-semibold mb-3">Author</h4>
            <div className="text-gray-400 text-sm space-y-2">
              <p className="text-white font-medium">
                Denzil Josteve Fernandes
              </p>
              <p>
                <a
                  href="mailto:denziljosteve@gmail.com"
                  className="hover:text-white transition-colors"
                >
                  📧 denziljosteve@gmail.com
                </a>
              </p>
              <p>
                <a
                  href="https://www.linkedin.com/in/denziljosteve"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-white transition-colors"
                >
                  💼 LinkedIn
                </a>
              </p>
              <p>
                <a
                  href="https://github.com/denziljosteve"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-white transition-colors"
                >
                  🐙 GitHub
                </a>
              </p>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-gray-800 mt-8 pt-6 text-center text-gray-400 text-sm">
          <p>
            © {currentYear} stockJEDI. Built with ❤️ by{" "}
            <a
              href="https://www.linkedin.com/in/denziljosteve"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-400 hover:text-blue-300 transition-colors"
            >
              Denzil Josteve Fernandes
            </a>
          </p>
          <p className="mt-2">
            Powered by FastAPI, Next.js, and AI
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

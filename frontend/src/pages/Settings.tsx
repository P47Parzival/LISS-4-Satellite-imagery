import React from 'react';
import { useTheme } from '../contexts/ThemeContext';

export default function Settings() {
  const { theme, toggleTheme } = useTheme();
  return (
    <div className="max-w-2xl mx-auto p-8">
      <h1 className="text-2xl font-bold mb-6">Settings</h1>
      <div className="bg-white dark:bg-gray-900 rounded-xl shadow p-6 mb-6">
        <div className="flex items-center justify-between">
          <span className="text-lg font-medium">Theme</span>
          <button
            onClick={toggleTheme}
            className="px-4 py-2 rounded-lg bg-gray-200 dark:bg-gray-800 text-gray-900 dark:text-gray-100 font-semibold focus:outline-none"
          >
            Switch to {theme === 'dark' ? 'Light' : 'Dark'} Mode
          </button>
        </div>
      </div>
      <div className="bg-white dark:bg-gray-900 rounded-xl shadow p-6">
        <span className="text-gray-500 dark:text-gray-400">More settings coming soon...</span>
      </div>
    </div>
  );
} 
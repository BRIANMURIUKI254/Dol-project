import React from 'react';
import Header from '@/components/Header';
import Hero from '@/components/Hero';
import About from '@/components/About';
import Houses from '@/components/Houses';
import Contact from '@/components/Contact';

const Index: React.FC = () => {
  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Header />
      <main className="flex-1">
        <section id="hero">
          <Hero />
        </section>
        <section id="about" className="py-16 bg-gray-50">
          <About />
        </section>
        <section id="houses" className="py-16 bg-white">
          <Houses />
        </section>
        <section id="contact" className="py-16 bg-gray-50">
          <Contact />
        </section>
      </main>
      <footer className="bg-gray-900 text-gray-300 text-center py-6">
        <p>© {new Date().getFullYear()} D.O.L Ministries. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default Index;

import React from 'react';
import Header from '@/components/Header';
import Hero from '@/components/Hero';
import About from '@/components/About';
import Houses from '@/components/Houses';
import Contact from '@/components/Contact';

const Index: React.FC = () => {
  return (
    <div className="bg-background flex flex-col overflow-x-hidden">
      <Header />
      <main className="pt-8">
        <section id="hero">
          <Hero />
        </section>
        <section id="about" className="py-0 bg-gray-50">
          <About />
        </section>
        <section id="houses" className="bg-white">
          <Houses />
        </section>
        <section id="contact" className="bg-gray-50">
          <Contact />
        </section>
      </main>
    </div>
  );
};

export default Index;

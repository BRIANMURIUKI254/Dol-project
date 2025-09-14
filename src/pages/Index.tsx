import Header from '@/components/Header';
import Hero from '@/components/Hero';
import About from '@/components/About';
import Houses from '@/components/Houses';
import Contact from '@/components/Contact';

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main>
        <Hero />
        <About />
        <Houses />
        <Contact />
      </main>
    </div>
  );
};

export default Index;

import { Button } from '@/components/ui/button';
import { ArrowRight, Star } from 'lucide-react';

const Hero = () => {
  return (
    <section id="home" className="relative py-8 md:py-12 flex items-center justify-center overflow-hidden">
      {/* Background with divine gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-background via-accent/30 to-primary/10" />
      
      {/* Decorative stars */}
      <div className="absolute inset-0 overflow-hidden">
        <Star className="absolute top-20 left-10 text-primary/30 h-4 w-4 animate-pulse" />
        <Star className="absolute top-32 right-16 text-primary/40 h-6 w-6 animate-pulse delay-300" />
        <Star className="absolute bottom-40 left-20 text-primary/20 h-5 w-5 animate-pulse delay-700" />
        <Star className="absolute bottom-60 right-10 text-primary/35 h-4 w-4 animate-pulse delay-500" />
        <Star className="absolute top-1/2 left-1/4 text-primary/25 h-3 w-3 animate-pulse delay-1000" />
        <Star className="absolute top-1/3 right-1/3 text-primary/30 h-5 w-5 animate-pulse delay-200" />
      </div>

      <div className="relative z-10 container mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <div className="max-w-4xl mx-auto">
          {/* Main heading */}
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-foreground mb-6 leading-tight">
            Days of{' '}
            <span className="bg-gradient-to-r from-primary to-primary-light bg-clip-text text-transparent">
              Light
            </span>
          </h1>
          
          {/* Subtitle */}
          <p className="text-xl md:text-2xl text-primary font-semibold mb-4 tracking-wide">
            Full of Glory
          </p>
          
          {/* Mission statement */}
          <p className="text-lg md:text-xl text-muted-foreground max-w-3xl mx-auto mb-8 leading-relaxed">
            A movement that seeks to see the word of God prevail and be glorified amongst men through the teaching and demonstration of the wisdom and power of God which is Jesus Christ our Lord.
          </p>

          {/* Ministry verse highlight */}
          <div className="bg-card/80 backdrop-blur-sm border border-border rounded-lg p-6 mb-8 max-w-2xl mx-auto shadow-gentle">
            <p className="text-foreground font-medium italic text-base md:text-lg">
              "That the God of our Lord Jesus Christ, the Father of glory, may give unto you the spirit of wisdom and revelation in the knowledge of him"
            </p>
            <p className="text-primary font-semibold mt-2">- Ephesians 1:17</p>
          </div>

          {/* Call to action buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Button 
              size="lg" 
              className="bg-primary hover:bg-primary-dark text-primary-foreground shadow-divine group"
            >
              Join Our Fellowship
              <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
            </Button>
            <Button 
              variant="outline" 
              size="lg"
              className="border-primary text-primary hover:bg-primary hover:text-primary-foreground"
            >
              Watch Sermons
            </Button>
          </div>
        </div>
      </div>

      {/* Bottom fade */}
      <div className="absolute bottom-0 left-0 right-0 h-20 bg-gradient-to-t from-background to-transparent" />
    </section>
  );
};

export default Hero;
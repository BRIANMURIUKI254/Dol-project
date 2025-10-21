import { Card, CardContent } from '@/components/ui/card';
import { Target, Eye, BookOpen } from 'lucide-react';

const About = () => {
  return (
    <section className="pt-0 pb-0 bg-gradient-to-b from-background to-accent/20">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 pb-0">
        {/* Section header */}
        <div className="text-center mb-8">
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
            What is Days of Light?
          </h2>
          <div className="w-24 h-1 bg-gradient-to-r from-primary to-primary-light mx-auto rounded-full" />
        </div>

        {/* Main description */}
        <div className="max-w-4xl mx-auto text-center mb-8">
          <p className="text-lg md:text-xl text-muted-foreground leading-relaxed">
            Days of Light is a movement that seeks to see the word of God prevail and be glorified amongst men through the teaching and demonstration of the wisdom and power of God which is Jesus Christ our Lord. We stand to be counted amongst many in the massive move of the spirit that God is doing in this tail-end of the end of the days, where the earth shall be filled with the knowledge of the glory of the Lord as the waters cover the sea.
          </p>
        </div>

        {/* Vision, Mission, History cards */}
        <div className="grid md:grid-cols-3 gap-8 mb-8">
          {/* Vision */}
          <Card className="group hover:shadow-divine transition-all duration-300">
            <CardContent className="p-8 text-center">
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-6 group-hover:bg-primary/20 transition-colors">
                <Eye className="h-8 w-8 text-primary" />
              </div>
              <h3 className="text-xl font-bold text-foreground mb-4">Vision</h3>
              <p className="text-muted-foreground leading-relaxed">
                To stand as witnesses of the Godhead as a communion of believers.
              </p>
            </CardContent>
          </Card>

          {/* Mission */}
          <Card className="group hover:shadow-divine transition-all duration-300">
            <CardContent className="p-8 text-center">
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-6 group-hover:bg-primary/20 transition-colors">
                <Target className="h-8 w-8 text-primary" />
              </div>
              <h3 className="text-xl font-bold text-foreground mb-4">Mission</h3>
              <p className="text-muted-foreground leading-relaxed">
                Groom men in God by the ministry of the word and prayer that they be counted in the end-time army of our Lord Jesus.
              </p>
            </CardContent>
          </Card>

          {/* History */}
          <Card className="group hover:shadow-divine transition-all duration-300">
            <CardContent className="p-8 text-center">
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-6 group-hover:bg-primary/20 transition-colors">
                <BookOpen className="h-8 w-8 text-primary" />
              </div>
              <h3 className="text-xl font-bold text-foreground mb-4">History</h3>
              <p className="text-muted-foreground leading-relaxed">
                Started in November 2019 at Kenyatta University, beginning with a small fellowship that has grown into a thriving online and offline community.
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Ministry verses */}
        <div className="bg-card border border-border rounded-lg p-8 md:p-12 shadow-gentle mb-0">
          <h3 className="text-2xl font-bold text-center text-foreground mb-8">Ministry Verses</h3>
          <div className="max-w-3xl mx-auto space-y-4">
            <div className="flex">
              <span className="text-primary font-bold mr-4 text-lg">17</span>
              <p className="text-muted-foreground leading-relaxed">
                That the God of our Lord Jesus Christ, the Father of glory, may give unto you the spirit of wisdom and revelation in the knowledge of him:
              </p>
            </div>
            <div className="flex">
              <span className="text-primary font-bold mr-4 text-lg">18</span>
              <p className="text-muted-foreground leading-relaxed">
                The eyes of your understanding being enlightened; that ye may know what the hope of his calling is, and what the riches of the glory of his inheritance in the saints,
              </p>
            </div>
            <div className="flex">
              <span className="text-primary font-bold mr-4 text-lg">19</span>
              <p className="text-muted-foreground leading-relaxed">
                And what is the exceeding greatness of his power to us-ward who believe, according to the working of his mighty power,
              </p>
            </div>
            <div className="flex">
              <span className="text-primary font-bold mr-4 text-lg">20</span>
              <p className="text-muted-foreground leading-relaxed">
                Which he wrought in Christ, when he raised him from the dead, and set him at his own right hand in the heavenly places,
              </p>
            </div>
            <p className="text-primary font-semibold text-center mt-6">- Ephesians 1:17-20 KJV</p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;
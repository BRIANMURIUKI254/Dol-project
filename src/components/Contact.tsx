import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Mail, MessageCircle, Instagram, Facebook, Youtube, Music, Smartphone } from 'lucide-react';

const Contact = () => {
  const socialLinks = [
    {
      name: 'Telegram',
      icon: MessageCircle,
      url: 'https://t.me/daysoflightfullofglory',
      description: 'Join our community channel'
    },
    {
      name: 'Instagram',
      icon: Instagram,
      url: 'https://www.instagram.com/daysoflight_dol/',
      description: 'Follow our daily updates'
    },
    {
      name: 'Facebook',
      icon: Facebook,
      url: 'https://www.facebook.com/DaysofLightfullofglory/',
      description: 'Connect with our community'
    },
    {
      name: 'YouTube',
      icon: Youtube,
      url: 'https://www.youtube.com/@daysoflight',
      description: 'Watch our sermons and events'
    },
    {
      name: 'Spotify',
      icon: Music,
      url: 'https://open.spotify.com/show/4tGuXXqYEuEOmAYNoG7m0E?si=euMl5HG_Q7-kayc8Wb9W',
      description: 'Listen to our podcast'
    },
    {
      name: 'Mobile App',
      icon: Smartphone,
      url: 'https://play.google.com/store/apps/details?id=apps.carlpeters.dol',
      description: 'Download our app'
    }
  ];

  return (
    <section id="contact" className="pt-8 md:pt-12 pb-4 md:pb-6 bg-gradient-to-b from-background to-accent/20">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section header */}
        <div className="text-center mb-8">
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
            Connect With Us
          </h2>
          <div className="w-24 h-1 bg-gradient-to-r from-primary to-primary-light mx-auto rounded-full mb-4" />
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Join our growing community and stay connected through our various platforms.
          </p>
        </div>

        <div className="max-w-4xl mx-auto">
          {/* Contact information */}
          <div className="text-center mb-12">
            <Card className="bg-card/80 backdrop-blur-sm border border-primary/20 shadow-divine">
              <CardContent className="p-8">
                <div className="flex flex-col items-center mb-6">
                  <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mb-4">
                    <Mail className="h-8 w-8 text-primary" />
                  </div>
                  <h3 className="text-xl font-bold text-foreground mb-2">Get In Touch</h3>
                </div>
                
                <div className="space-y-4">
                  <div>
                    <p className="text-muted-foreground mb-2">Email us at:</p>
                    <a 
                      href="mailto:daysoflightfullofglory@gmail.com"
                      className="text-primary hover:text-primary-dark font-semibold text-lg transition-colors"
                    >
                      daysoflightfullofglory@gmail.com
                    </a>
                  </div>
                  
                  <div className="pt-4 border-t border-border">
                    <p className="text-muted-foreground">
                      We'd love to hear from you. Whether you have questions about our ministry, 
                      want to join a house fellowship, or need prayer, don't hesitate to reach out.
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Social media links */}
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
            {socialLinks.map((social, index) => {
              const IconComponent = social.icon;
              return (
                <Card 
                  key={index} 
                  className="group hover:shadow-divine transition-all duration-300 hover:-translate-y-1"
                >
                  <CardContent className="p-6">
                    <div className="flex flex-col items-center text-center">
                      <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mb-4 group-hover:bg-primary/20 transition-colors">
                        <IconComponent className="h-6 w-6 text-primary" />
                      </div>
                      <h4 className="font-semibold text-foreground mb-2 group-hover:text-primary transition-colors">
                        {social.name}
                      </h4>
                      <p className="text-sm text-muted-foreground mb-4">
                        {social.description}
                      </p>
                      <Button 
                        asChild
                        variant="outline" 
                        size="sm"
                        className="border-primary text-primary hover:bg-primary hover:text-primary-foreground"
                      >
                        <a 
                          href={social.url} 
                          target="_blank" 
                          rel="noopener noreferrer"
                        >
                          Connect
                        </a>
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>

          {/* Ministry leader section */}
          <div className="text-center">
            <Card className="bg-gradient-to-r from-primary/5 to-primary-light/5 border border-primary/20">
              <CardContent className="p-8">
                <h3 className="text-2xl font-bold text-foreground mb-4">
                  Ministry Lead Steward
                </h3>
                <h4 className="text-xl font-semibold text-primary mb-4">
                  Pastor Kelvin Muli
                </h4>
                <p className="text-muted-foreground leading-relaxed max-w-2xl mx-auto">
                  Led by divine calling and passionate about seeing God's word prevail and be glorified. 
                  Pastor Kelvin guides Days of Light with wisdom and revelation, committed to grooming 
                  believers for the end-time harvest.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Contact;
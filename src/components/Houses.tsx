import { Card, CardContent } from '@/components/ui/card';
import { MapPin, Clock, Calendar, Loader2 } from 'lucide-react';
import { useHouses } from '@/hooks/useApi';

const Houses = () => {
  const { data: housesData, isLoading, error } = useHouses();

  // Fallback static data in case API fails
  const fallbackHouses = [
    {
      id: 1,
      name: 'House of Thika',
      day: 'Monday',
      time: '5:00pm - 8:00pm',
      location: 'CCI Arise and Shine, next to Eton Hotel',
      is_active: true,
    },
    {
      id: 2,
      name: 'House of Rongai',
      day: 'Monday',
      time: '5:30pm - 8:00pm',
      location: 'Maasai Lodge Opposite Think twice',
      is_active: true,
    },
    {
      id: 3,
      name: 'House of Murang\'a',
      day: 'Tuesday',
      time: '6:30pm - 8:30pm',
      location: 'Cool Palace, B7',
      is_active: true,
    },
    {
      id: 4,
      name: 'House of KU',
      day: 'Monday',
      time: '5:00pm - 8:00pm',
      location: 'Kahawa Sukari near Suburbs',
      is_active: true,
    },
    {
      id: 5,
      name: 'House of Kitengela',
      day: 'Wednesday',
      time: '6:00pm - 8:00pm',
      location: 'Balozi road (immediately after Imani apartments) House 001',
      is_active: true,
    },
    {
      id: 6,
      name: 'House of AIU',
      day: 'Coming Soon',
      time: 'TBA',
      location: 'Location to be announced',
      is_active: false,
    },
  ];

  // Use API data if available, otherwise fallback to static data
  const houses = housesData?.results || fallbackHouses;

  return (
    <section id="houses" className="py-16 md:py-24 bg-accent/10">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section header */}
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
            Our Houses
          </h2>
          <div className="w-24 h-1 bg-gradient-to-r from-primary to-primary-light mx-auto rounded-full mb-4" />
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Join us for fellowship and worship at one of our house meetings across different locations.
          </p>
          
          {/* Loading indicator */}
          {isLoading && (
            <div className="flex items-center justify-center mt-8">
              <Loader2 className="h-6 w-6 animate-spin text-primary" />
              <span className="ml-2 text-muted-foreground">Loading houses...</span>
            </div>
          )}
          
          {/* Error message */}
          {error && (
            <div className="mt-8 p-4 bg-destructive/10 border border-destructive/20 rounded-lg">
              <p className="text-destructive text-sm">
                Unable to load houses from server. Showing cached data.
              </p>
            </div>
          )}
        </div>

        {/* Houses grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {houses.map((house, index) => (
            <Card 
              key={index} 
              className="group hover:shadow-divine transition-all duration-300 hover:-translate-y-1"
            >
              <CardContent className="p-6">
                <div className="mb-6">
                  <h3 className="text-xl font-bold text-foreground mb-2 group-hover:text-primary transition-colors">
                    {house.name}
                  </h3>
                  <div className="w-12 h-1 bg-primary rounded-full" />
                </div>

                <div className="space-y-4">
                  {/* Day */}
                  <div className="flex items-center text-muted-foreground">
                    <Calendar className="h-5 w-5 text-primary mr-3 flex-shrink-0" />
                    <span className="font-medium">{house.day}</span>
                  </div>

                  {/* Time */}
                  <div className="flex items-center text-muted-foreground">
                    <Clock className="h-5 w-5 text-primary mr-3 flex-shrink-0" />
                    <span>{house.time}</span>
                  </div>

                  {/* Location */}
                  <div className="flex items-start text-muted-foreground">
                    <MapPin className="h-5 w-5 text-primary mr-3 flex-shrink-0 mt-0.5" />
                    <span className="leading-relaxed">{house.location}</span>
                  </div>
                </div>

                {house.name !== 'House of AIU' && (
                  <div className="mt-6 pt-4 border-t border-border">
                    <p className="text-sm text-primary font-medium">
                      All are welcome to join us!
                    </p>
                  </div>
                )}

                {house.name === 'House of AIU' && (
                  <div className="mt-6 pt-4 border-t border-border">
                    <p className="text-sm text-muted-foreground italic">
                      Details coming soon
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Call to action */}
        <div className="text-center mt-16">
          <div className="bg-card border border-primary/20 rounded-lg p-8 max-w-2xl mx-auto shadow-gentle">
            <h3 className="text-xl font-bold text-foreground mb-4">
              Can't find a house near you?
            </h3>
            <p className="text-muted-foreground mb-6">
              We're always looking to start new houses. Get in touch with us to explore starting a fellowship in your area.
            </p>
            <a 
              href="#contact" 
              className="inline-flex items-center text-primary hover:text-primary-dark font-semibold transition-colors"
            >
              Contact us to learn more
            </a>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Houses;
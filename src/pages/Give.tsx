import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Helmet } from 'react-helmet-async';

export default function Give() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <Helmet>
        <title>Give | D.O.L</title>
        <meta name="description" content="Support D.O.L through donations or by becoming a partner" />
      </Helmet>

      {/* Hero Section */}
      <div className="bg-blue-600 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">Partner With Us</h1>
          <p className="text-xl md:text-2xl max-w-3xl mx-auto">
            Your support enables us to continue our mission and make a lasting impact in our community.
          </p>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-2 gap-8">
            {/* Giving Card */}
            <Card className="border-2 border-blue-100 shadow-lg hover:shadow-xl transition-shadow duration-300">
              <CardHeader className="bg-blue-50 rounded-t-lg">
                <CardTitle className="text-2xl font-bold text-blue-800">Giving</CardTitle>
              </CardHeader>
              <CardContent className="p-6">
                <div className="space-y-6">
                  <div className="bg-white p-6 rounded-lg border border-blue-100">
                    <h3 className="text-lg font-semibold mb-2 text-gray-800">M-Pesa Till Number</h3>
                    <div className="text-3xl font-bold text-blue-600 mb-1">9350131</div>
                    <p className="text-gray-600">Purity Buyanzi Mukhwana</p>
                  </div>
                  <div className="prose text-gray-600">
                    <p>Use the Till Number above to make your donation through M-Pesa.</p>
                    <p className="mt-2">Your generous support helps us continue our mission and expand our impact.</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Become a Partner Card */}
            <Card className="border-2 border-green-100 shadow-lg hover:shadow-xl transition-shadow duration-300">
              <CardHeader className="bg-green-50 rounded-t-lg">
                <CardTitle className="text-2xl font-bold text-green-800">Become a Partner</CardTitle>
              </CardHeader>
              <CardContent className="p-6">
                <div className="space-y-6 h-full flex flex-col">
                  <div className="prose text-gray-600 flex-grow">
                    <p>Join us in our mission by becoming a partner. Your partnership will help us create lasting change in our community.</p>
                    <p className="mt-4">As a partner, you'll receive regular updates about our work and the impact of your support.</p>
                  </div>
                  <div className="mt-auto">
                    <Button 
                      asChild 
                      size="lg" 
                      className="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-6 text-lg"
                    >
                      <a 
                        href="https://forms.gle/your-google-form-id" 
                        target="_blank" 
                        rel="noopener noreferrer"
                      >
                        Apply to be a Partner
                      </a>
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Additional Information */}
          <div className="mt-16 text-center max-w-3xl mx-auto">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Other Ways to Give</h2>
            <p className="text-gray-600 mb-6">
              For alternative donation methods or more information about our giving programs, 
              please contact us at <a href="mailto:daysoflightfullofglory@gmail.com" className="text-blue-600 hover:underline">info@dol.org</a>.
            </p>
            <p className="text-sm text-gray-500">
              D.O.L is a registered non-profit organization. All donations are tax-deductible to the fullest extent allowed by law.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

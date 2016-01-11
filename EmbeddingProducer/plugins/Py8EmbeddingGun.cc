
#include "GeneratorInterface/Core/interface/GeneratorFilter.h"
#include "GeneratorInterface/ExternalDecays/interface/ExternalDecayDriver.h"

#include "GeneratorInterface/Pythia8Interface/interface/Py8GunBase.h"

// EvtGen plugin
//
//#include "Pythia8Plugins/EvtGen.h" //needed in next versions


namespace gen {
  
class Py8EmbeddingGun : public Py8GunBase {
   
 public:
      
    Py8EmbeddingGun( edm::ParameterSet const& );
    ~Py8EmbeddingGun() {}
	 
    bool generatePartonsAndHadronize() override;
    const char* classname() const override;
	 
 private:
      
    // EGun particle(s) characteristics
    double  fMinEta;
    double  fMaxEta;
    double  fMinE ;
    double  fMaxE ;
    bool    fAddAntiParticle;
};


Py8EmbeddingGun::Py8EmbeddingGun( edm::ParameterSet const& ps )
   : Py8GunBase(ps) 
{

   // ParameterSet defpset ;
  // edm::ParameterSet pgun_params = 
   //   ps.getParameter<edm::ParameterSet>("PGunParameters"); // , defpset ) ;
   //fMinEta     = pgun_params.getParameter<double>("MinEta"); // ,-2.2);
   //fMaxEta     = pgun_params.getParameter<double>("MaxEta"); // , 2.2);
   //fMinE       = pgun_params.getParameter<double>("MinE"); // ,  0.);
   //fMaxE       = pgun_params.getParameter<double>("MaxE"); // ,  0.);
   //fAddAntiParticle = pgun_params.getParameter<bool>("AddAntiParticle"); //, false) ;  

}



bool Py8EmbeddingGun::generatePartonsAndHadronize(){
  
  fMasterGen->event.reset();
  double mass = 91;
  double px = 100;
  double py = 100;
  double pz = 10;
  
  double ee=sqrt(px*px+py*py+pz*pz+mass*mass);
  
  (fMasterGen->event).append( 23, 1, 0, 0, px, py, pz, ee, mass ); 
  
  if ( !fMasterGen->next() ) return false;
  event().reset(new HepMC::GenEvent);
  
  return toHepMC.fill_next_event( fMasterGen->event, event().get() );
  
}






  
const char* Py8EmbeddingGun::classname() const
{
   return "Py8EmbeddingGun"; 
}


typedef edm::GeneratorFilter<gen::Py8EmbeddingGun, gen::ExternalDecayDriver> Pythia8EmbeddingGun;
  
}  // end namespace


using gen::Pythia8EmbeddingGun;
DEFINE_FWK_MODULE(Pythia8EmbeddingGun);
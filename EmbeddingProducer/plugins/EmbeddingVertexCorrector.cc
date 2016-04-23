#ifndef __EmbeddingVertexCorrector__
#define __EmbeddingVertexCorrector__

#include "IOMC/EventVertexGenerators/interface/BaseEvtVtxGenerator.h"
#include "DataFormats/Math/interface/Point3D.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"

namespace CLHEP {
   class HepRandomEngine;
}

class EmbeddingVertexCorrector : public BaseEvtVtxGenerator
{
   private:
      
      HepMC::FourVector* vtx = nullptr;
      
      edm::EDGetTokenT<math::XYZPoint> vertex_position_token;
      
   public:
      
      EmbeddingVertexCorrector(const edm::ParameterSet & iConfig) : BaseEvtVtxGenerator(iConfig)
      {
         vertex_position_token = consumes<math::XYZPoint>(edm::InputTag("vertexPosition"));
      };
      ~EmbeddingVertexCorrector() {};
      
      HepMC::FourVector* newVertex(CLHEP::HepRandomEngine* engine)
      {
         return vtx;
      };
      
      TMatrixD* GetInvLorentzBoost()
      {
         return 0;
      }
      
      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
      
      void produce( edm::Event& iEvent, const edm::EventSetup& iSetup)
      {
         edm::Handle<math::XYZPoint> vertex_position;
         iEvent.getByToken(vertex_position_token, vertex_position);
         std::cout << vertex_position.product()->x() << std::endl;
         BaseEvtVtxGenerator::produce(iEvent, iSetup);
      };
};

void
EmbeddingVertexCorrector::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

DEFINE_FWK_MODULE(EmbeddingVertexCorrector);
#endif

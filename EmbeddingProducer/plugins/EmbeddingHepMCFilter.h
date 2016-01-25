#ifndef __EMBEDDINGHEPMCFILTER__
#define __EMBEDDINGHEPMCFILTER__

#include "GeneratorInterface/Core/interface/BaseHepMCFilter.h"

class EmbeddingHepMCFilter : public BaseHepMCFilter{
    
    public:
        
        explicit EmbeddingHepMCFilter(const edm::ParameterSet &);
        ~EmbeddingHepMCFilter();
        
        
        virtual bool filter(const HepMC::GenEvent* evt);
        
    private:
        
        const int tauonPDGID_ = 15;
        const int muonPDGID_ = 13;
        const int electronPDGID_ = 11;
        double ptCut_;
        double absEtaCut_;
        bool switchToMuonEmbedding_;
    
};


EmbeddingHepMCFilter::EmbeddingHepMCFilter(const edm::ParameterSet & iConfig)
{
    ptCut_ = iConfig.getParameter<double>("ptCut");
    absEtaCut_ = iConfig.getParameter<double>("absEtaCut");
    switchToMuonEmbedding_ = iConfig.getParameter<bool>("switchToMuonEmbedding");
}

EmbeddingHepMCFilter::~EmbeddingHepMCFilter()
{
}


bool
EmbeddingHepMCFilter::filter(const HepMC::GenEvent* evt)
{
    bool passed_first = false;
    bool passed_second = false;
    for ( HepMC::GenEvent::particle_const_iterator particle = evt->particles_begin(); particle != evt->particles_end(); ++particle )
    {
        // TauonEmbedding
        if (std::abs((*particle)->pdg_id()) == tauonPDGID_ && !switchToMuonEmbedding_)
        {
            for ( HepMC::GenVertex::particle_iterator daughter =(*particle)->end_vertex()->particles_begin(HepMC::children); daughter != (*particle)->end_vertex()->particles_end(HepMC::children); ++daughter )
            {
                bool leptonic_decay = std::abs((*daughter)->pdg_id()) == muonPDGID_ || std::abs((*daughter)->pdg_id()) == electronPDGID_;
                if ( leptonic_decay && (*daughter)->momentum().perp() > ptCut_  && std::abs((*daughter)->momentum().eta()) < absEtaCut_)
                {
                    if (passed_first) passed_second = true;
                    else passed_first = true;
                }
            }
        }
        // MuonEmbedding
        else if (std::abs((*particle)->pdg_id()) == muonPDGID_ && switchToMuonEmbedding_)
        {
            if ( (*particle)->momentum().perp() > ptCut_  && std::abs((*particle)->momentum().eta()) < absEtaCut_)
            {
                if (passed_first) passed_second = true;
                else passed_first = true;
            }
        }
    }
    std::cout << "passed: " << (passed_first && passed_second) << std::endl;
    return (passed_first && passed_second);
}

#endif

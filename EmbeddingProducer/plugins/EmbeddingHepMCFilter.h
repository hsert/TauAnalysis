#ifndef __EMBEDDINGHEPMCFILTER__
#define __EMBEDDINGHEPMCFILTER__

#include "GeneratorInterface/Core/interface/BaseHepMCFilter.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

class EmbeddingHepMCFilter : public BaseHepMCFilter{
    
    public:
        
        explicit EmbeddingHepMCFilter(const edm::ParameterSet &);
        ~EmbeddingHepMCFilter();
        
        
        virtual bool filter(const HepMC::GenEvent* evt);
        virtual void decay_and_sump4Vis(HepMC::GenParticle* particle, reco::Candidate::LorentzVector &p4Vis);
        
    private:
        
        const int tauon_neutrino_PDGID_ = 16;
        const int tauonPDGID_ = 15;
        const int muon_neutrino_PDGID_ = 14;
        const int muonPDGID_ = 13;
        const int electron_neutrino_PDGID_ = 12;
        const int electronPDGID_ = 11;
        
        double ptCut_;
        double absEtaCut_;
        bool switchToMuonEmbedding_;
        
        enum class TauDecayMode : int
        {
            Muon = 1,
            Electron = 2,
            Hadronic = 3
        };
        
        std::vector<TauDecayMode> DecayChannel_;
        std::vector<reco::Candidate::LorentzVector> p4VisPair_;
    
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
    if (switchToMuonEmbedding_) return true; // Do nothing, if MuonEmbedding enabled.
    
    bool passed_first = false;
    bool passed_second = false;
    reco::Candidate::LorentzVector p4Vis_all;
    // Going through the particle list. Mother particles are allways before their children. 
    // One can stop the loop after the second tau is reached and processed.
    for ( HepMC::GenEvent::particle_const_iterator particle = evt->particles_begin(); particle != evt->particles_end(); ++particle )
    {
        //(*particle)->print();
        bool neutrino = (std::abs((*particle)->pdg_id()) == tauon_neutrino_PDGID_) ||
                        (std::abs((*particle)->pdg_id()) == muon_neutrino_PDGID_) ||
                        (std::abs((*particle)->pdg_id()) == electron_neutrino_PDGID_);
        
        if ((*particle)->status() == 1 && !neutrino) p4Vis_all += (reco::Candidate::LorentzVector) (*particle)->momentum();
        if (std::abs((*particle)->pdg_id()) == tauonPDGID_)
        {
            reco::Candidate::LorentzVector p4Vis;
            decay_and_sump4Vis((*particle), p4Vis);
            p4VisPair_.push_back(p4Vis);
            std::cout << "visible Px: " << p4Vis.Px() << std::endl;
        }
    }
    std::cout << "visible Px all: " << p4Vis_all.Px() << std::endl;
    return (passed_first && passed_second);
}

void
EmbeddingHepMCFilter::decay_and_sump4Vis(HepMC::GenParticle* particle, reco::Candidate::LorentzVector &p4Vis)
{
    for (HepMC::GenVertex::particle_iterator daughter = particle->end_vertex()->particles_begin(HepMC::children); 
    daughter != particle->end_vertex()->particles_end(HepMC::children); ++daughter)
    {
        bool neutrino = (std::abs((*daughter)->pdg_id()) == tauon_neutrino_PDGID_) ||
                        (std::abs((*daughter)->pdg_id()) == muon_neutrino_PDGID_) ||
                        (std::abs((*daughter)->pdg_id()) == electron_neutrino_PDGID_);
        
        // Determining DecayMode, if particle is tauon.
        if (std::abs(particle->pdg_id()) == tauonPDGID_)
        {
            if (std::abs((*daughter)->pdg_id()) == muonPDGID_) DecayChannel_.push_back(TauDecayMode::Muon);
            else if (std::abs((*daughter)->pdg_id()) == electronPDGID_) DecayChannel_.push_back(TauDecayMode::Electron);
            else DecayChannel_.push_back(TauDecayMode::Hadronic);
        }
        // Adding up all visible momentum in recursive way.
        if ((*daughter)->status() == 1 && !neutrino) p4Vis += (reco::Candidate::LorentzVector) (*daughter)->momentum();
        else if (!neutrino) decay_and_sump4Vis((*daughter), p4Vis);
    }
}

#endif

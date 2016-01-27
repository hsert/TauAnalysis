#ifndef __EMBEDDINGHEPMCFILTER__
#define __EMBEDDINGHEPMCFILTER__

#include "GeneratorInterface/Core/interface/BaseHepMCFilter.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

class EmbeddingHepMCFilter : public BaseHepMCFilter{
    
    private:
        
        const int tauon_neutrino_PDGID_ = 16;
        const int tauonPDGID_ = 15;
        const int muon_neutrino_PDGID_ = 14;
        const int muonPDGID_ = 13;
        const int electron_neutrino_PDGID_ = 12;
        const int electronPDGID_ = 11;
        
        bool switchToMuonEmbedding_;
        std::map<std::string, std::string> cuts = {
            {"ElEl", "ElEl"},
            {"MuMu", "MuMu"},
            {"HadHad", "HadHad"},
            {"ElMu", "ElMu"},
            {"ElHad", "ElHad"},
            {"MuHad", "MuHad"}
        };
        
        enum class TauDecayMode : int
        {
            Unfilled = -1,
            Muon = 0,
            Electron = 1,
            Hadronic = 2
        };
        
        std::string return_mode(TauDecayMode mode)
        {
            if (mode == TauDecayMode::Muon) return "Mu";
            else if (mode ==  TauDecayMode::Electron) return "El";
            else if (mode == TauDecayMode::Hadronic) return "Had";
            else return "Undefined";
        }
        
        
        struct DecayChannel
        {
            TauDecayMode first = TauDecayMode::Unfilled;
            TauDecayMode second = TauDecayMode::Unfilled;
            
            void fill(TauDecayMode mode)
            {
                if (first == TauDecayMode::Unfilled) first = mode;
                else if (second == TauDecayMode::Unfilled) second = mode;
            };
            void reset()
            {
                first = TauDecayMode::Unfilled;
                second = TauDecayMode::Unfilled;
            }
            void reverse()
            {
               TauDecayMode tmp = first;
               first = second;
               second = tmp;
            }
        };
        
        std::vector<reco::Candidate::LorentzVector> p4VisPair_;
        DecayChannel DecayChannel_;
        
        virtual void decay_and_sump4Vis(HepMC::GenParticle* particle, reco::Candidate::LorentzVector &p4Vis);
        virtual void sort_by_convention(DecayChannel& dc, std::vector<reco::Candidate::LorentzVector> &p4VisPair);
        virtual bool apply_cuts(DecayChannel& dc, std::vector<reco::Candidate::LorentzVector> &p4VisPair);
        virtual void str_replace(std::string &s, const std::string &search, const std::string &replace);
        
    public:
        
        explicit EmbeddingHepMCFilter(const edm::ParameterSet &);
        ~EmbeddingHepMCFilter();
        
        virtual bool filter(const HepMC::GenEvent* evt);
        
};


EmbeddingHepMCFilter::EmbeddingHepMCFilter(const edm::ParameterSet & iConfig)
{
    switchToMuonEmbedding_ = iConfig.getParameter<bool>("switchToMuonEmbedding");
    for (auto & cut : cuts)
    {
        // cut.first is the key in the map, cut.second the value
        cut.second = iConfig.getParameter<std::string>(cut.first + "Cut");
        std::cout << cut.first << " : " << cut.second << std::endl;
    }
    std::cout << cuts["MuHad"] << std::endl;
}

EmbeddingHepMCFilter::~EmbeddingHepMCFilter()
{
}


bool
EmbeddingHepMCFilter::filter(const HepMC::GenEvent* evt)
{
    if (switchToMuonEmbedding_) return true; // Do nothing, if MuonEmbedding enabled.
    
    //Reset DecayChannel_ and p4VisPair_ at the beginning of each event.
    DecayChannel_.reset();
    p4VisPair_.resize(0);
    
    reco::Candidate::LorentzVector p4Vis_all;
    // Going through the particle list. Mother particles are allways before their children. 
    // One can stop the loop after the second tau is reached and processed.
    for ( HepMC::GenEvent::particle_const_iterator particle = evt->particles_begin(); particle != evt->particles_end(); ++particle )
    {
        bool neutrino = (std::abs((*particle)->pdg_id()) == tauon_neutrino_PDGID_) ||
                        (std::abs((*particle)->pdg_id()) == muon_neutrino_PDGID_) ||
                        (std::abs((*particle)->pdg_id()) == electron_neutrino_PDGID_);
        
        if ((*particle)->status() == 1 && !neutrino) p4Vis_all += (reco::Candidate::LorentzVector) (*particle)->momentum();
        if (std::abs((*particle)->pdg_id()) == tauonPDGID_)
        {
            reco::Candidate::LorentzVector p4Vis;
            decay_and_sump4Vis((*particle), p4Vis); // recursive access to final states.
            p4VisPair_.push_back(p4Vis);
            std::cout << "visible Px: " << p4Vis.Px() << std::endl;
        }
    }
    std::cout << "visible Px all: " << p4Vis_all.Px() << std::endl;
    std::cout << "p4VisPair size: " << p4VisPair_.size() << std::endl;
    // Putting DecayChannel_ in default convention:
    // For mixed decay channels use the Electron_Muon, Electron_Hadronic, Muon_Hadronic convention.
    // For symmetric decay channels (e.g. Muon_Muon) use Leading_Trailing convention with respect to Pt.
    std::cout << "DecayChannel: " << return_mode(DecayChannel_.first) << return_mode(DecayChannel_.second) << std::endl;
    sort_by_convention(DecayChannel_, p4VisPair_);
    std::cout << "DecayChannel: " << return_mode(DecayChannel_.first) << return_mode(DecayChannel_.second) << std::endl;
    return apply_cuts(DecayChannel_, p4VisPair_);
}


void
EmbeddingHepMCFilter::decay_and_sump4Vis(HepMC::GenParticle* particle, reco::Candidate::LorentzVector &p4Vis)
{
    bool decaymode_known = false;
    for (HepMC::GenVertex::particle_iterator daughter = particle->end_vertex()->particles_begin(HepMC::children); 
    daughter != particle->end_vertex()->particles_end(HepMC::children); ++daughter)
    {
        bool neutrino = (std::abs((*daughter)->pdg_id()) == tauon_neutrino_PDGID_) ||
                        (std::abs((*daughter)->pdg_id()) == muon_neutrino_PDGID_) ||
                        (std::abs((*daughter)->pdg_id()) == electron_neutrino_PDGID_);
        
        // Determining DecayMode, if particle is tauon. Asuming, that there are only the two tauons from the Z-boson.
        // This is the case for the simulated Z->tautau event constructed by EmbeddingLHEProducer. 
        if (std::abs(particle->pdg_id()) == tauonPDGID_ && !decaymode_known)
        {
            if (std::abs((*daughter)->pdg_id()) == muonPDGID_)
            {
                DecayChannel_.fill(TauDecayMode::Muon);
                decaymode_known = true;
            }
            else if (std::abs((*daughter)->pdg_id()) == electronPDGID_)
            {
                DecayChannel_.fill(TauDecayMode::Electron);
                decaymode_known = true;
            }
            else if (!neutrino)
            {
                DecayChannel_.fill(TauDecayMode::Hadronic);
                decaymode_known = true;
            }
        }
        // Adding up all visible momentum in recursive way.
        if ((*daughter)->status() == 1 && !neutrino) p4Vis += (reco::Candidate::LorentzVector) (*daughter)->momentum();
        else if (!neutrino) decay_and_sump4Vis((*daughter), p4Vis);
    }
}


void
EmbeddingHepMCFilter::sort_by_convention(DecayChannel &dc, std::vector<reco::Candidate::LorentzVector> &p4VisPair)
{
    bool mixed_false_order = (dc.first == TauDecayMode::Hadronic && dc.second == TauDecayMode::Muon) ||
                             (dc.first == TauDecayMode::Hadronic && dc.second == TauDecayMode::Electron) ||
                             (dc.first == TauDecayMode::Muon && dc.second == TauDecayMode::Electron);
    
    if (dc.first == dc.second && p4VisPair[0].Pt() < p4VisPair[1].Pt())
    {
        std::cout << "Changing symmetric channels to Leading_Trailing convention in Pt" << std::endl;
        std::cout << "Pt's before: " << p4VisPair[0].Pt() << " " << p4VisPair[1].Pt() << std::endl;
        std::reverse(p4VisPair.begin(),p4VisPair.end());
        std::cout << "Pt's after: " << p4VisPair[0].Pt() << " " << p4VisPair[1].Pt() << std::endl;
    }
    else if (mixed_false_order)
    {
        std::cout << "Swapping order of mixed channels" << std::endl;
        std::cout << "Pt's before: " << p4VisPair[0].Pt() << " " << p4VisPair[1].Pt() << std::endl;
        dc.reverse();
        std::cout << "DecayChannel: " << return_mode(dc.first) << return_mode(dc.second) << std::endl;
        std::reverse(p4VisPair.begin(),p4VisPair.end());
        std::cout << "Pt's after: " << p4VisPair[0].Pt() << " " << p4VisPair[1].Pt() << std::endl;
    }
}

bool
EmbeddingHepMCFilter::apply_cuts(DecayChannel &dc, std::vector<reco::Candidate::LorentzVector> &p4VisPair)
{
    bool mixed = (dc.first == TauDecayMode::Muon && dc.second == TauDecayMode::Hadronic) ||
                 (dc.first == TauDecayMode::Electron && dc.second == TauDecayMode::Hadronic) ||
                 (dc.first == TauDecayMode::Electron && dc.second == TauDecayMode::Muon);
    
    std::string dc_str = return_mode(dc.first) + return_mode(dc.second);
    std::string cut_str = cuts[dc_str];
    if (mixed)
    {
        str_replace(cut_str,return_mode(dc.first), "begin");
        str_replace(cut_str,return_mode(dc.second), "end");
    }
    else if (dc.first == dc.second)
    {
        str_replace(cut_str,return_mode(dc.first)+"1", "begin");
        str_replace(cut_str,return_mode(dc.second)+"2", "end");
    }
    std::cout << cut_str << std::endl;
    //StringCutObjectSelector<reco::Candidate::LorentzVector> select(cut_str);
    return true;
}

// http://www.emoticode.net/c-plus-plus/replace-all-substring-occurrences-in-std-string.html
void
EmbeddingHepMCFilter::str_replace(std::string &s, const std::string &search, const std::string &replace) 
{
    for(size_t pos = 0;;pos += replace.length())
    {
        pos = s.find( search, pos);
        if(pos == std::string::npos) break;

        s.erase(pos,search.length());
        s.insert(pos,replace);
    }
}

#endif

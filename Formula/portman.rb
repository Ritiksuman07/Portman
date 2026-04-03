class Portman < Formula
  desc "Local port and process manager for developers"
  homepage "https://github.com/ritiksuman07/portman"
  url "https://github.com/ritiksuman07/portman/archive/refs/tags/v1.0.0.tar.gz"
  sha256 ""
  license "MIT"

  def install
    system "go", "build", "-o", bin/"portman", "."
  end

  test do
    system "#{bin}/portman", "--help"
  end
end
